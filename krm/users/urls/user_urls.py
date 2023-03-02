# -*- encoding: utf-8 -*-

"""Users urls."""

from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.users.views import (
    DashboardView,

    CaDashboardView,
    GaDashboardView,
    RuDashboardView,

    GaUserListView,
    GaUserCreateView,
    GaUserUpdateView,
    GaUserDeleteView,
    GaUserDetailView,
    GaUserImportView,
)


urlpatterns = [
    path(
        'dashboard-redirect/',
        DashboardView.as_view(),
        name='dashboard'
    ),
    path(
        'ga-dashboard/',
        GaDashboardView.as_view(),
        name='ga_dashboard'
    ),
    path(
        'ca-dashboard/',
        CaDashboardView.as_view(),
        name='ca_dashboard'
    ),
    path(
        'ru-dashboard/',
        RuDashboardView.as_view(),
        name='ru_dashboard'
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
    path("import_users/",
         GaUserImportView.as_view(), name="ga_import_users"),
]
