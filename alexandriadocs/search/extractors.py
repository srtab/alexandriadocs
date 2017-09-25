# -*- coding: utf-8 -*-
from django.utils.html import strip_tags
from lxml.etree import ParserError
from lxml.html.clean import Cleaner
from pyquery import PyQuery


class HtmlExtractor(object):
    """
    Extract relevant content from html document.

    ``kill_tags``:
        A list of tags to kill. Killing also removes the tag's content,
        i.e. the whole subtree, not just the tag itself.

    ``content_tags``:
        A list of tags to search the most relevant content from the document.
        Order of tags is important, only the first match will be used.

    ``title_tags``:
        A list of tags to search title of document. Order of tags is important,
        only the first match will be used.
    """

    kill_tags = ['footer']
    content_tags = ['[role=main]', 'body']
    title_tags = ['h1', 'h2', 'head title']

    def __init__(self, html):
        self.doc = PyQuery(html)

    @property
    def content(self):
        """ """
        for path in self.content_tags:
            try:
                content = self.doc(path).html()
                if not content:
                    continue
                return self.strip_all(content)
            except ValueError:
                continue
        return None

    @property
    def title(self):
        """ """
        for path in self.title_tags:
            try:
                title = self.doc(path).eq(0).html()
                if not title:
                    continue
                return self.strip_all(title)
            except ValueError:
                continue
        return None

    def strip_all(self, html):
        """
        Clean html content striping all html tags and removing all inline
        script and style.
        """
        try:
            cleaner = Cleaner(style=True, kill_tags=self.kill_tags)
            cleaned_html = cleaner.clean_html(html)
            text = strip_tags(cleaned_html).replace('¶', '')
        except ParserError:
            return ""
        return " ".join(text.split())
