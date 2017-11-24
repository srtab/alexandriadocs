# -*- coding: utf-8 -*-
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import UpdateView

from accounts.forms import ProfileUpdateForm
from core.views import AlexandriaDocsSEO


@method_decorator(login_required, name='dispatch')
class ProfileUpdateView(AlexandriaDocsSEO, SuccessMessageMixin, UpdateView):
    """ """
    model = get_user_model()
    title = _("Profile")
    form_class = ProfileUpdateForm
    success_message = _("%(username)s profile was updated successfully")
    template_name = 'account/user_form.html'
