# -*- encoding: utf-8 -*-
"""Users views."""
import hashlib

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


@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'users/Dashboard.html'

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseRedirect(reverse('manuscripts:manuscript_list_ru'))

        return super(DashboardView, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super(DashboardView, self).get_context_data(**kwargs)
        return context


@method_decorator(decorators, name='dispatch')
class LoginView(FormView):

    # template_name = 'users/UsersLogin.html'
    form_class = LoginForm

    template_name = 'pages/auth/signin.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile(
        #     'js/custom/authentication/sign-up/general.js')

        # Define the layout for this module
        # _templates/layout/auth.html
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
            login(self.request, user)
            return HttpResponseRedirect(
                reverse('users:dashboard')
            )

        else:
            messages.add_message(
                self.request, messages.ERROR, _('Usuario no válido'))
            return super(LoginView, self).form_invalid(form)


class RememberPassword(FormView):
    form_class = RememberForm
    template_name = 'users/UsersRememberPassword.html'
    success_url = reverse_lazy('users:remember_password_email_sended')

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
    template_name = 'users/UsersTypePassword.html'

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
        return reverse_lazy('users:login')


class LoginCode(FormView):
    form_class = LoginCodeForm
    template_name = 'users/UsersLoginCode.html'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        login_code = kwargs['login_code']
        try:
            self.user = User.objects.get(login_code=login_code)
        except User.DoesNotExist:
            raise Http404
        return super(LoginCode, self).dispatch(
            request, request, *args, **kwargs)

    def form_valid(self, form):
        # Comprobamos si el código metido, haciéndole el md5, es igual que el parámetro de la url

        if hashlib.md5(form.cleaned_data['login_code'].encode()).hexdigest() == self.kwargs['login_code']:
            login(self.request, self.user)
            return super(LoginCode, self).form_valid(form)
        else:
            messages.add_message(
                self.request,
                messages.ERROR,
                ('Código de inicio de sesión erróneo')
            )
            return super(
                LoginCode,
                self
            ).form_invalid(form)

    def get_success_url(self):
        if self.user.is_superuser:
            return reverse('users:dashboard')
        else:
            return reverse('manuscripts:manuscript_list_ru')


class RememberEmailSended(TemplateView):
    template_name = 'users/UsersPasswordResetOk.html'


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('users:login'))
