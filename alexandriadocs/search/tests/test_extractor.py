# -*- coding: utf-8 -*-
from unittest.mock import Mock

from django.test import SimpleTestCase
from pyquery import PyQuery
from search.extractors import HtmlExtractor


class HtmlExtractorText(SimpleTestCase):

    def test_init(self):
        extractor = HtmlExtractor("<div></div>")
        self.assertIsNotNone(extractor.doc)
        self.assertIsInstance(extractor.doc, PyQuery)

    def test_content(self):
        doc = "<body>Dummy Content</body>"
        extractor = HtmlExtractor(doc)
        self.assertEqual(extractor.content, "Dummy Content")

    def test_content_no_body(self):
        doc = "<div>Dummy Content</div>"
        extractor = HtmlExtractor(doc)
        self.assertIsNone(extractor.content)

    def test_content_raise_value_error(self):
        extractor = HtmlExtractor("<div></div>")
        extractor.doc = Mock(side_effect=ValueError())
        self.assertIsNone(extractor.content)

    def test_title(self):
        doc = "<h1>Dummy Title</h1>"
        extractor = HtmlExtractor(doc)
        self.assertEqual(extractor.title, "Dummy Title")

    def test_content_no_title(self):
        doc = "<div>Dummy Title</div>"
        extractor = HtmlExtractor(doc)
        self.assertIsNone(extractor.title)

    def test_title_raise_value_error(self):
        extractor = HtmlExtractor("<h1></h1>")
        extractor.doc = Mock(side_effect=ValueError())
        self.assertIsNone(extractor.title)
