# -*- encoding: utf-8 -*-
"""Users views."""
import hashlib
import json
import time
import urllib

from saml2 import (
    BINDING_HTTP_POST,
    BINDING_HTTP_REDIRECT,
    entity,
)
from saml2.client import Saml2Client
from saml2.config import Config as Saml2Config

from django.utils.module_loading import import_string

from authlib.integrations.django_client import OAuth
from django.conf import settings

from django.contrib.auth import login, authenticate, logout
from datetime import date
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.shortcuts import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import get_object_or_404
from django.db.models import Count

from django.contrib import messages

from django.utils import translation

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    RedirectView
)

from django.contrib.auth.decorators import login_required
from django.utils.http import url_has_allowed_host_and_scheme

from krm.users.decorators import (
    is_global_admin,
    # is_business_group_admin
)

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.users.forms import LoginForm, RememberForm, PasswordForm, LoginCodeForm
from krm.users.models import User


decorators = [
    csrf_protect,
    never_cache,
]

if (settings.DEBUG_LOGIN):
    oauth = OAuth()

    oauth.register(
        "auth0",
        client_id= settings.AUTH0_CLIENT_ID,
        client_secret= settings.AUTH0_CLIENT_SECRET,
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f"https://dev-njl8nr7c8xdkfs74.us.auth0.com/.well-known/openid-configuration",
    )

@method_decorator(login_required, name='dispatch')
class DashboardView(RedirectView):

    def get_redirect_url(self, **kwargs):
        if self.request.user.is_superuser:
            return reverse("users:ga_dashboard")
        elif self.request.user.is_company_admin:
            return reverse("users:ca_dashboard")
        else:
            return reverse("users:ru_dashboard")
        
@method_decorator(decorators, name='dispatch')
class LoginView(FormView):
    template_name = 'users/login/UserLogin.html'
    form_class = LoginForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('users:dashboard'))

        else:
            return super(LoginView, self).dispatch(
                request, request,
                *args, **kwargs
            )


    def form_valid(self, form):
        usuario = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        user = authenticate(username=usuario, password=password)

        if user is not None:
            from django.utils import translation
            translation.activate('es')
            login(self.request, user)
            return HttpResponseRedirect(
                reverse('users:dashboard')
            )

        else:
            messages.add_message(
                self.request, messages.ERROR, _('Usuario no válido'))
            return super(LoginView, self).form_invalid(form)

class RememberPassword(FormView):
    template_name = 'users/login/UsersRememberPassword.html'
    form_class = RememberForm
    success_url = reverse_lazy('auth:remember_password_email_sended')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        try:
            user = User.objects.get(username=email)
        except User.DoesNotExist:
            msg = _('No existe usuario con ese email')
            form._errors['email'] = [msg]
            return super(RememberPassword, self).form_invalid(form)

        user.send_email_remember_password()
        return super(RememberPassword, self).form_valid(form)

class TypeYourPassword(FormView):
    form_class = PasswordForm
    template_name = 'users/login/UsersTypePassword.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context

    def get_initial(self):
        return {
            'remember_key': self.kwargs.get('remember_key')
        }

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        remember_key = kwargs['remember_key']
        if User.objects.filter(remember_key=remember_key).count() == 0:
            self.user = None
            messages.add_message(
                self.request, messages.ERROR,
                _('Enlace caducado, vuelva a solicitar recordar contraseña'))

            return HttpResponseRedirect(reverse_lazy('auth:remember_password_form'))
        else:
            self.user = User.objects.get(remember_key=remember_key)
        return super(TypeYourPassword, self).dispatch(
            request, request, *args, **kwargs)

    def form_valid(self, form):
        self.user.set_password(form.data['password2'])
        self.user.save()
        # self.user.add_action(_('Reset password'))
        return super(TypeYourPassword, self).form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS,
            _('Password cambiado correctamente'))
        return reverse_lazy('auth:login')

class RememberEmailSended(TemplateView):
    template_name = 'users/login/UsersPasswordResetOk.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context.update({
            'layout': KTTheme.setLayout('auth.html', context),
        })
        return context


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('auth:login'))
