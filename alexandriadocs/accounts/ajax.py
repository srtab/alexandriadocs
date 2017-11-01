# -*- coding: utf-8 -*-
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils.decorators import method_decorator

from accounts.models import User
from allauth.account.models import EmailAddress
from core.views import BaseSelect2View


@method_decorator(login_required, name='dispatch')
class UserAutocompleteView(BaseSelect2View):
    """ """
    model = User

    def get_queryset(self):
        qs = User.objects.filter(is_active=True)
        if self.term:
            emails = EmailAddress.objects.filter(
                email__icontains=self.term, verified=True)
            return qs.filter(
                Q(username__icontains=self.term) |
                Q(name__icontains=self.term) |
                Q(pk__in=emails.values('user_id')))
        return qs
