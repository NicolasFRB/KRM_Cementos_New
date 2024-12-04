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

# oauth = OAuth()

# oauth.register(
#     "auth0",
#     client_id="1Dk3p7qRl4ETYA9emXHwooqES1wuVN5S",
#     client_secret="Hs-F46aKi3a-4NDz0aS9LgJtBSGAadpSngPNb0TbLqOGoHyLejo00OHg2_wYFzOV",
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url=f"https://dev-njl8nr7c8xdkfs74.us.auth0.com/.well-known/openid-configuration",
# )

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


# class LoginView(RedirectView):

#     def get_redirect_url(self, **kwargs):
#         return oauth.auth0.authorize_redirect(self.request, self.request.build_absolute_uri(reverse("users:dashboard")))

# # Login
def login_view(r):
    # try:
    #     import urlparse as _urlparse
    #     from urllib import unquote
    # except:
    #     import urllib.parse as _urlparse
    #     from urllib.parse import unquote
    # next_url = r.GET.get('next', _default_next_url())

    # try:
    #     if 'next=' in unquote(next_url):
    #         next_url = _urlparse.parse_qs(_urlparse.urlparse(unquote(next_url)).query)['next'][0]
    # except:
    #     next_url = r.GET.get('next', _default_next_url())

    # # Only permit signin requests where the next_url is a safe URL
    # url_ok = url_has_allowed_host_and_scheme(next_url, None)

    # if not url_ok:
    #     return HttpResponseRedirect(reverse()) # to reverse

    # r.session['login_next_url'] = next_url

    # saml_client = _get_saml_client(get_current_domain(r))
    # _, info = saml_client.prepare_for_authenticate()

    # redirect_url = None

    # for key, value in info['headers']:
    #     if key == 'Location':
    #         redirect_url = value
    #         break

    return HttpResponseRedirect("https://identity-services.uat.elcorteingles.es/samlsso?spEntityID=https://krm-tool-uat.des-onprem1.eci.geci/en/auth/callback/")


    # return oauth.auth0.authorize_redirect(
    #     request, request.build_absolute_uri(reverse("auth:callback"))
    # )

# class CallbackView(RedirectView):

#     def get_redirect_url(self, **kwargs):
#         token = oauth.auth0.authorize_access_token(self.request)
#         self.request.session["user"] = token
#         return HttpResponseRedirect(self.request.build_absolute_uri(reverse("users:dashboard")))
    

# CALLBACK DEPENDENCIES BEGIN
# def get_reverse(objs):
#     '''In order to support different django version, I have to do this '''
#     if parse_version(get_version()) >= parse_version('2.0'):
#         from django.urls import reverse
#     else:
#         from django.core.urlresolvers import reverse
#     if objs.__class__.__name__ not in ['list', 'tuple']:
#         objs = [objs]

#     for obj in objs:
#         try:
#             return reverse(obj)
#         except:
#             pass
#     raise Exception('We got a URL reverse issue: %s. This is a known issue but please still submit a ticket at https://github.com/fangli/django-saml2-auth/issues/new' % str(objs))

def _get_metadata():
    # if 'METADATA_LOCAL_FILE_PATH' in settings.SAML2_AUTH:
        return {
            'local': [settings.SAML2_AUTH['METADATA_LOCAL_FILE_PATH']]
        }
    # else:
    #     return {
    #         'remote': [
    #             {
    #                 "url": settings.SAML2_AUTH['METADATA_AUTO_CONF_URL'],
    #             },
    #         ]
    #     }

def get_current_domain(r):
    if 'ASSERTION_URL' in settings.SAML2_AUTH:
        return settings.SAML2_AUTH['ASSERTION_URL']
    return '{scheme}://{host}'.format(
        scheme='https' if r.is_secure() else 'http',
        host=r.get_host(),
    )

def _default_next_url():
    if 'DEFAULT_NEXT_URL' in settings.SAML2_AUTH:
        return settings.SAML2_AUTH['DEFAULT_NEXT_URL']
    # Lazily evaluate this in case we don't have admin loaded.
    return reverse('users:dashboard')

def _create_new_user(username, email, name):
    user = User.objects.create_user(username, email)
    user.name = name
    # user.last_name = lastname

    # groups = [Group.objects.get(name=x) for x in settings.SAML2_AUTH.get('NEW_USER_PROFILE', {}).get('USER_GROUPS', [])]
    # user.groups.set(groups)

    user.is_active = settings.SAML2_AUTH.get('NEW_USER_PROFILE', {}).get('ACTIVE_STATUS', True)
    user.is_staff = settings.SAML2_AUTH.get('NEW_USER_PROFILE', {}).get('STAFF_STATUS', True)
    user.is_superuser = settings.SAML2_AUTH.get('NEW_USER_PROFILE', {}).get('SUPERUSER_STATUS', False)
    user.save()
    return user

def _get_saml_client(domain):
    acs_url = domain + reverse("auth:callback")
    metadata = _get_metadata()

    saml_settings = {
        'xmlsec_binary': '/usr/bin/xmlsec1',  # Asegúrate de que esta ruta es correcta
        'metadata': metadata,
        'service': {
            'sp': {
                'endpoints': {
                    'assertion_consumer_service': [
                        (acs_url, BINDING_HTTP_REDIRECT),
                        (acs_url, BINDING_HTTP_POST)
                    ],
                },
                'allow_unsolicited': True,
                'authn_requests_signed': False,
                'logout_requests_signed': True,
                'want_assertions_signed': True,
                'want_response_signed': True,
            },
        },
    }

    if 'ENTITY_ID' in settings.SAML2_AUTH:
        saml_settings['entityid'] = settings.SAML2_AUTH['ENTITY_ID']

    # if 'NAME_ID_FORMAT' in settings.SAML2_AUTH:
    #     saml_settings['service']['sp']['name_id_format'] = settings.SAML2_AUTH['NAME_ID_FORMAT']

    spConfig = Saml2Config()
    spConfig.load(saml_settings)
    spConfig.allow_unknown_attributes = True
    saml_client = Saml2Client(config=spConfig)
    return saml_client
# CALLBACK DEPENDENCIES END

@csrf_exempt
def callback_view(r):
    saml_client = _get_saml_client(get_current_domain(r))
    resp = r.POST.get('SAMLResponse', None)
    next_url = r.session.get('login_next_url', _default_next_url())

    if not resp:
        return HttpResponseRedirect(reverse("auth:logout")) #to denied login

    authn_response = saml_client.parse_authn_request_response(
        resp, entity.BINDING_HTTP_POST)
    if authn_response is None:
        print("Auth Response equals None")
        return HttpResponseRedirect(reverse("auth:logout")) #to denied login

    user_identity = authn_response.get_identity()
    if user_identity is None:
        print("UserIdentity equals None")
        return HttpResponseRedirect(reverse("auth:logout")) #to denied login

    # print(user_identity)
    user_email = user_identity[settings.SAML2_AUTH.get('ATTRIBUTES_MAP', {}).get('email', 'email')][0]
    user_name = user_identity[settings.SAML2_AUTH.get('ATTRIBUTES_MAP', {}).get('username', 'username')][0]
    user_real_name = user_identity[settings.SAML2_AUTH.get('ATTRIBUTES_MAP', {}).get('name', 'username')][0]
    # user_last_name = user_identity[settings.SAML2_AUTH.get('ATTRIBUTES_MAP', {}).get('last_name', 'http://schemas.xmlsoap.org/ws/2005/05/identity/claims/surname')][0]

    target_user = None
    is_new_user = False

    try:
        target_user = User.objects.get(username=user_email)
        # if settings.SAML2_AUTH.get('TRIGGER', {}).get('BEFORE_LOGIN', None):
        #     import_string(settings.SAML2_AUTH['TRIGGER']['BEFORE_LOGIN'])(user_identity)
    except User.DoesNotExist:
        print("User does not exist")
        new_user_should_be_created = settings.SAML2_AUTH.get('CREATE_USER', True)
        if new_user_should_be_created: 
            target_user = _create_new_user(user_name, user_email, user_real_name)
            # if settings.SAML2_AUTH.get('TRIGGER', {}).get('CREATE_USER', None):
            #     import_string(settings.SAML2_AUTH['TRIGGER']['CREATE_USER'])(user_identity)
            is_new_user = True
        else:
            return HttpResponseRedirect(reverse("auth:logout")) # to denied

    r.session.flush()

    if target_user.is_active:
        target_user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(r, target_user)
    else:
        return HttpResponseRedirect(reverse("auth:logout")) # to denied 

    if settings.SAML2_AUTH.get('USE_JWT') is True:
        # We use JWT auth send token to frontend
        jwt_token = jwt_encode(target_user)
        query = '?uid={}&token={}'.format(target_user.id, jwt_token)

        frontend_url = settings.SAML2_AUTH.get(
            'FRONTEND_URL', next_url)

        return HttpResponseRedirect(frontend_url+query)

    if is_new_user:
        # try:
        return HttpResponseRedirect(reverse("users:dashboard"))
        # except TemplateDoesNotExist:
        #     return HttpResponseRedirect(next_url)
    else:
        return HttpResponseRedirect(reverse("users:dashboard"))
    
    # token = oauth.auth0.authorize_access_token(request)
    
    # user = authenticate(username=token['userinfo']['nickname'], password=token['access_token'])
    # request.session["user"] = user
    # print("TOKEN")
    # print(token)
    # print("step1", user)
    # if user is not None:
    #     print("step2")
    #     from django.utils import translation
    #     translation.activate('es')
    #     login(request, user)
    #     return HttpResponseRedirect(
    #         reverse('users:dashboard')
    #     )

    # else:
    #     print("step3")
    #     messages.add_message(request, messages.ERROR, _('Usuario no válido'))
    #     return HttpResponseRedirect(reverse('auth:logout'))



# class LogoutView(RedirectView):

#     def get_redirect_url(self, **kwargs):
#         self.request.session.clear()

#         return HttpResponseRedirect(
#             f"https://dev-njl8nr7c8xdkfs74.us.auth0.com/v2/logout?"
#                 + urllib.parse.urlencode(
#                     {
#                         "returnTo": self.request.build_absolute_uri(reverse("users:dashboard")),
#                         "client_id": "1Dk3p7qRl4ETYA9emXHwooqES1wuVN5S",
#                     },
#                     quote_via=urllib.parse.quote_plus,
#                 )
#         )
    
def logout_view(request):
    request.session.clear()
# https://identity-services.uat.elcorteingles.es/samlsso?spEntityID=https://krm-tool-uat.des-onprem1.eci.geci/en/auth/callback/&slo=true&returnTo=https://krm-tool-uat.des-onprem1.eci.geci/en/auth/logout
# https://identity-services.uat.elcorteingles.es/samlsso?spEntityID=https://krm-tool-uat.des-onprem1.eci.geci/en/auth/callback/
    return HttpResponseRedirect(
        "https://identity-services.uat.elcorteingles.es/samlsso?slo=true"
        # f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        # + urllib.parse.urlencode(
        #     {
        #         "returnTo": request.build_absolute_uri(reverse("users:dashboard")),
        #         "client_id": settings.AUTH0_CLIENT_ID,
        #     },
        #     quote_via=urllib.parse.quote_plus,
        # ),
    )

# @method_decorator(decorators, name='dispatch')
# class LoginView(FormView):
#     template_name = 'users/login/UserLogin.html'
#     form_class = LoginForm

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


# @login_required   
# def logout_view(request):
#     logout(request)
#     return HttpResponseRedirect(reverse('auth:login'))
