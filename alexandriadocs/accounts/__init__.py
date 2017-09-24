from django.utils.module_loading import autodiscover_modules


def autodiscover():
    autodiscover_modules('access_checkers')


default_app_config = 'accounts.apps.AccountsConfig'
