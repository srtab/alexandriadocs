# -*- coding: utf-8 -*-
from accounts.forms import ProfileUpdateForm
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(SuccessMessageMixin, UpdateView):
    """ """
    model = get_user_model()
    form_class = ProfileUpdateForm
    success_message = _("%(username)s profile was updated successfully")
