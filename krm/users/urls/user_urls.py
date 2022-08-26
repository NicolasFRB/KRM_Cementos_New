# -*- encoding: utf-8 -*-

"""Users urls."""

from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.users.views import (
    DashboardView,
    GaUserListView,
    GaUserCreateView,
    GaUserUpdateView,
    GaUserDeleteView,
    GaUserDetailView,
)


urlpatterns = [
    path(
        'dashboard/',
        DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        '',
        GaUserListView.as_view(),
        name='ga_user_list'
    ),
    path(
        'new-user/',
        GaUserCreateView.as_view(),
        name='ga_user_create'
    ),
    path(
        'detail/<pk>/',
        GaUserDetailView.as_view(),
        name='ga_user_detail'
    ),
    path(
        'update/<pk>/',
        GaUserUpdateView.as_view(),
        name='ga_user_update'
    ),
    path(
        'delete/<pk>/',
        GaUserDeleteView.as_view(),
        name='ga_user_delete'
    ),
    path(
        'create/',
        GaUserCreateView.as_view(),
        name='ga_user_create'
    ),
]
