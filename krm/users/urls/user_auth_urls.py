# -*- encoding: utf-8 -*-

"""Users urls."""

from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.users.views import (
    LoginView,
    logout_view,
    RememberPassword,
    TypeYourPassword,
    RememberEmailSended,
)


urlpatterns = [
    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    path(
        'logout/',
        logout_view,
        name='logout'
    ),
    path(
        'reset-password/',
        RememberPassword.as_view(),
        name='remember_password_form'
    ),
    re_path(
        'reset-password/type-your-password/(?P<remember_key>[0-9a-f]{32})/',
        TypeYourPassword.as_view(),
        name='type_your_password'
    ),
    path(
        'reset-password/email-sended/',
        RememberEmailSended.as_view(),
        name='remember_password_email_sended'
    ),
]
