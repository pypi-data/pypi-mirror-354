import fnmatch
import re
import os
import sys
import logging

import mkdocs
import mkdocs.plugins
import mkdocs.structure.files

from mkdocs.config import Config
from mkdocs.structure.files import Files
from mkdocs.structure.nav import Navigation
from mkdocs.structure.pages import Page
from mkdocs.utils.templates import TemplateContext

logger = logging.getLogger("mkdocs.plugins")

class ExcludePlugin(mkdocs.plugins.BasePlugin):

    config_scheme = (
        ('globs', mkdocs.config.config_options.Type((str,list), default=None)),
        ('regex', mkdocs.config.config_options.Type((str, list), default=None)),
    )

    def __init__(self):
        self.enabled = True
        self.total_time = 0

    def on_serve(self, server, config, **kwargs):
        return server

    def on_pre_build(self, config):
        return

    def on_files(self, files, config):
        globs = self.config['globs'] or []
        if not isinstance(globs, list):
            globs = [globs]

        regexes = self.config['regex'] or []
        if not isinstance(regexes, list):
            regexes = [regexes]

        def include(name):
            for g in globs:
                if fnmatch.fnmatchcase(name, g):
                    return False
            for r in regexes:
                if re.match(r, name):
                    return False
            return True

        out = []
        for f in files:
            if not include(f.src_path): continue 
            out.append(f)
        
        return mkdocs.structure.files.Files(out)
        # return files

    def on_nav(self, nav, config, files):
        return nav

    def on_env(self, env, config, files):
        return env

    def on_config(self, config):
        return config

    def on_post_build(self, config):
        return

    def on_pre_template(self, template, template_name, config):
        return template

    def on_template_context(self, context, template_name, config):
        return context
    
    def on_post_template(self, output_content, template_name, config):
        return output_content
    
    def on_pre_page(self, page, config, files):
        return page

    def on_page_markdown(self, markdown, page, config, files):
        return markdown

    def on_page_content(self, html, page, config, files):
        return html

    def on_page_context(self, context, page, config, nav):
        return context

    def on_post_page(self, output_content, page, config):
        return output_content
