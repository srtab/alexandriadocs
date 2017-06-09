# -*- coding: utf-8 -*-
from __future__ import unicode_literals, absolute_import

from haystack.forms import SearchForm as HaystackSearchForm


class SearchForm(HaystackSearchForm):

    def search(self):
        if not self.is_valid():
            return self.no_query_found()

        sqs = self.searchqueryset.auto_query(self.cleaned_data['q'])

        if self.load_all:
            sqs = sqs.load_all()

        return sqs
