# -*- coding: utf-8 -*-
from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        super().ready()
        self.module.autodiscover()
