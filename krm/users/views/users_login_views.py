# -*- encoding: utf-8 -*-
"""Users views."""
import hashlib

from urllib.parse import quote_plus, urlencode
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
from django.views.decorators.csrf import csrf_protect
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

oauth = OAuth()

oauth.register(
    "auth0",
    client_id="1Dk3p7qRl4ETYA9emXHwooqES1wuVN5S",
    client_secret="Hs-F46aKi3a-4NDz0aS9LgJtBSGAadpSngPNb0TbLqOGoHyLejo00OHg2_wYFzOV",
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

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context = KTLayout.init(context)
    #     breadcrums = [
    #         {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
    #     ]
    #     context['page_title'] = _(
    #         'Dashboard para el Administrador de Compañía')
    #     context['breadcrums'] = breadcrums
    #     return context


class LoginView(RedirectView):
    # template_name = 'users/login/UserLogin.html'
    def get_redirect_url(self, **kwargs):
        return oauth.auth0.authorize_redirect(
            self.request, self.request.build_absolute_uri(reverse("users:dashboard"))
        )

# # Login
# def login_view(request):
#     return oauth.auth0.authorize_redirect(
#         request, request.build_absolute_uri(reverse("users:callback"))
#     )

class CallbackView(RedirectView):

    def get_redirect_url(self, **kwargs):
        token = oauth.auth0.authorize_access_token(self.request)
        self.request.session["user"] = token
        return HttpResponseRedirect(self.request.build_absolute_uri(reverse("users:dashboard")))
    

# def callback_view(request):
#     token = oauth.auth0.authorize_access_token(request)
#     request.session["user"] = token
#     return HttpResponseRedirect(request.build_absolute_uri(reverse("users:dashboard")))


class LogoutView(RedirectView):

    def get_redirect_url(self, **kwargs):
        self.request.session.clear()

        return HttpResponseRedirect(
            f"https://dev-njl8nr7c8xdkfs74.us.auth0.com/v2/logout?"
            + urlencode(
                {
                    "returnTo": self.request.build_absolute_uri(reverse("users:dashboard")),
                    "client_id": "1Dk3p7qRl4ETYA9emXHwooqES1wuVN5S",
                },
                quote_via=quote_plus,
            ),
        )
    
# def logout_view(request):
#     request.session.clear()

#     return HttpResponseRedirect(
#         f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
#         + urlencode(
#             {
#                 "returnTo": request.build_absolute_uri(reverse("users:dashboard")),
#                 "client_id": settings.AUTH0_CLIENT_ID,
#             },
#             quote_via=quote_plus,
#         ),
#     )

# @method_decorator(decorators, name='dispatch')
# class LoginView(FormView):
#     template_name = 'users/login/UserLogin.html'
#     form_class = LoginForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)
#         context.update({
#             'layout': KTTheme.setLayout('auth.html', context),
#         })
#         return context

#     def dispatch(self, request, *args, **kwargs):
#         if request.user.is_authenticated:
#             return HttpResponseRedirect(reverse('users:dashboard'))

#         else:
#             return super(LoginView, self).dispatch(
#                 request, request,
#                 *args, **kwargs
#             )

#     def form_valid(self, form):
#         usuario = form.cleaned_data.get('username')
#         password = form.cleaned_data.get('password')
#         user = authenticate(username=usuario, password=password)

#         if user is not None:
#             from django.utils import translation
#             translation.activate('es')
#             login(self.request, user)
#             return HttpResponseRedirect(
#                 reverse('users:dashboard')
#             )

#         else:
#             messages.add_message(
#                 self.request, messages.ERROR, _('Usuario no válido'))
#             return super(LoginView, self).form_invalid(form)


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
        user = get_object_or_404(
            User, remember_key=self.kwargs.get('remember_key'))
        return {
            'remember_key': self.kwargs.get('remember_key')
        }

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        remember_key = kwargs['remember_key']
        try:
            self.user = User.objects.get(remember_key=remember_key)
        except User.DoesNotExist:
            raise Http404
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


# @login_required   
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('auth:login'))
