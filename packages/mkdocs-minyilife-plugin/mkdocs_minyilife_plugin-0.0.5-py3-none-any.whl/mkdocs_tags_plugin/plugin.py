import re
import logging

from collections import defaultdict
from markdown.extensions.toc import slugify

from mkdocs.config.config_options import Optional, Type
from mkdocs.config.base import Config
from mkdocs import utils

from mkdocs.config.defaults import MkDocsConfig
from mkdocs.plugins import BasePlugin
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext


# Set up logging
log = logging.getLogger("mkdocs.plugins")

class TagsPluginConfig(Config):
    enabled = Type(bool, default = True)

    # Settings for tags
    tags = Type(bool, default = True)
    tags_file = Optional(Type(str))

    # Settings for pays
    pay = Type(bool, default = False)
    pay_on_serve = Type(bool, default = True)

    # Settings for reviews
    review = Type(bool, default = False)
    review_on_serve = Type(bool, default = True)

    # Settings for disable render
    unrender = Type(bool, default = False)
    unrender_on_serve = Type(bool, default = False)

class TagsPlugin(BasePlugin[TagsPluginConfig]):
    supports_multiple_instances = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize incremental builds
        self.is_serve = False
        self.is_dirty = False

    # Determine whether we're serving the site
    def on_startup(self, *, command, dirty):
        self.is_serve = command == "serve"
        self.is_dirty = dirty

    def draft_enabled(self, page: Page):
        # draft: true
        return page.meta and page.meta.get("draft", False)

    def pay_enabled(self, page: Page):
        # pay: true
        return self.config.pay and page.meta and page.meta.get("pay", False)

    def review_enabled(self, page: Page):
        # review: true
        return self.config.review and page.meta and page.meta.get("review", False)

    def unrender_enabled(self, page: Page):
        # unrender: true
        return self.config.unrender and page.meta and page.meta.get("unrender", False)
    

    # Initialize plugin
    def on_config(self, config):
        if not self.config.enabled:
            return

        # Skip if tags should not be built
        if not self.config.tags:
            return

        # Initialize tags
        self.tags = defaultdict(list)
        self.tags_file = None

        # Retrieve tags mapping from configuration
        self.tags_map = config.extra.get("tags")

        # Use override of slugify function
        toc = { "slugify": slugify, "separator": "-" }
        if "toc" in config.mdx_configs:
            toc = { **toc, **config.mdx_configs["toc"] }

        # Partially apply slugify function
        self.slugify = lambda value: (
            toc["slugify"](str(value), toc["separator"])
        )

        # By default, pays are rendered when the documentation is served,
        # but not when it is built, for a better user experience
        if self.is_serve and self.config.pay_on_serve:
            self.config.pay = True

        if self.is_serve and self.config.review_on_serve:
            self.config.review = True

        if self.is_serve and self.config.unrender_on_serve:
            self.config.unrender = True

    # Hack: 2nd pass for tags index page(s)
    def on_nav(self, nav, config, files):
        if not self.config.enabled:
            return

        # Skip if tags should not be built
        if not self.config.tags:
            return

        # Resolve tags index page
        file = self.config.tags_file
        if file:
            self.tags_file = self._get_tags_file(files, file)

    # Build and render tags index page
    def on_page_markdown(self, markdown, page, config, files):
        if not self.config.enabled:
            return

        # Skip if tags should not be built
        if not self.config.tags:
            return

        # Skip, if page is excluded
        if page.file.inclusion.is_excluded():
            return

        # Render tags index page
        if page.file == self.tags_file:
            return self._render_tag_index(markdown)

        # Add page to tags index
        for tag in page.meta.get("tags", []):
            self.tags[tag].append(page)

    # Inject tags into page (after search and before minification)
    def on_page_context(self, context, page, config, nav):
        if not self.config.enabled:
            return

        # Skip if tags should not be built
        if not self.config.tags:
            return

        # Provide tags for page
        if "tags" in page.meta:
            context["tags"] = [
                self._render_tag(tag)
                    for tag in page.meta["tags"]
            ]

    # -------------------------------------------------------------------------

    # Obtain tags file
    def _get_tags_file(self, files, path):
        file = files.get_file_from_path(path)
        if not file:
            log.error(f"Tags file '{path}' does not exist.")
            sys.exit(1)

        # Add tags file to files
        files.remove(file)
        files.append(file)
        return file

    # Render tags index
    def _render_tag_index(self, markdown):
        if not "[TAGS]" in markdown:
            markdown += "\n[TAGS]"

        # Replace placeholder in Markdown with rendered tags index
        total_pages = set([page.file.src_uri for tag, pages in self.tags.items() for page in pages])
        total_pages_html = "- <span>Total " + str(len(total_pages)) + " Pages</span>\n"

        return markdown.replace("[TAGS]", total_pages_html + "\n".join([
            self._render_tag_links(*args)
                for args in sorted(self.tags.items())
        ]))

    # Render the given tag and links to all pages with occurrences
    def _render_tag_links(self, tag, pages):
        classes = ["md-tag"]
        if isinstance(self.tags_map, dict):
            classes.append("md-tag-icon")
            type = self.tags_map.get(tag)
            if type:
                classes.append(f"md-tag--{type}")

        # Render section for tag and a link to each page
        classes = " ".join(classes)
        content = [f"## <span class=\"{classes}\">{tag}</span>", ""]
        content.append(f"- <span>Total {len(pages)} Pages</span>")

        for page in sorted(pages, key=lambda x: x.url, reverse=True):
            url = utils.get_relative_url(
                page.file.src_uri,
                self.tags_file.src_uri
            )

            # Render link to page
            title = page.meta.get("title", page.title)
            content.append(f"- [{title}]({url})")

            if self.pay_enabled(page):
                content.append("<span class=\"md-draft md-pay\">Pay</span>")
            elif self.review_enabled(page):
                content.append("<span class=\"md-draft md-review\">Review</span>")
            elif self.draft_enabled(page):
                content.append("<span class=\"md-draft\">Draft</span>")
            else:
                pass

        # Return rendered tag links
        return "\n".join(content)

    # Render the given tag, linking to the tags index (if enabled)
    def _render_tag(self, tag):
        type = self.tags_map.get(tag) if self.tags_map else None
        if not self.tags_file or not self.slugify:
            return dict(name = tag, type = type)
        else:
            url = f"{self.tags_file.url}#{self.slugify(tag)}"
            return dict(name = tag, type = type, url = url)

    def on_files(self, files, *, config):
        if not self.config.enabled:
            return

        out = []
        for f in files:
            page = Page(None, f, config)
            if self._is_excluded(page): continue
            out.append(f)

        return Files(out)

    def _is_excluded(self, page:Page):
        # do not exclude any tags with serve mode
        if self.is_serve:
            return False

        # if not server mode, can't be draft/review/pay/unrender
        if self.draft_enabled(page) or self.pay_enabled(page) or self.review_enabled(page) or self.unrender_enabled(page):
            return True

    def on_page_content(self, html, *, page, config, files):
        if not hasattr(page, "config"):
            return html

        if self.draft_enabled(page):
            page.config.draft = True
        if self.review_enabled(page):
            page.config.review = True
        if self.pay_enabled(page):
            page.config.pay = True
        if self.unrender_enabled(page):
            page.config.unrender = True

        return html
