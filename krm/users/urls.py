# -*- encoding: utf-8 -*-

"""Users urls."""

from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.users.views import (
    DashboardView,
    LoginView,
    logout_view,
    RememberPassword,
    TypeYourPassword,
    RememberEmailSended,
    UserList,
    UserCreate,
    UserUpdate,
    UserDelete,
    UserDetail,
    # UserProfile,
    # UserProfileUpdate,
    # UserCompanyImport,
    # TestView
)


urlpatterns = [
    path(
        '',
        DashboardView.as_view(),
        name='dashboard'
    ),

    path(
        'login/',
        LoginView.as_view(),
        name='login'
    ),
    # re_path(
    #     'login/code/(?P<login_code>[0-9a-f]{32})/',
    #     LoginCode.as_view(),
    #     name='login_code'
    # ),
    path(
        'logout/',
        logout_view,
        name='logout'
    ),
    path(
        'users/',
        UserList.as_view(),
        name='user_list'
    ),
    path(
        'users/new-user/',
        UserCreate.as_view(),
        name='user_create'
    ),
    path(
        'users/<pk>/',
        UserDetail.as_view(),
        name='user_detail'
    ),
    path(
        'users/<pk>/update/',
        UserUpdate.as_view(),
        name='user_update'
    ),
    path(
        'users/<pk>/delete/',
        UserDelete.as_view(),
        name='user_delete'
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
