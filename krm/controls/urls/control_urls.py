from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.controls.views import (
    GaControlListView,
    GaControlCreateView,
    GaControlDeleteView,
    GaControlDetailView,
    GaControlUpdateView,
    GaControlImport
)


urlpatterns = [
    path(
        '',
        GaControlListView.as_view(),
        name='ga_control_list'
    ),
    path(
        'detail/<pk>/',
        GaControlDetailView.as_view(),
        name='ga_control_detail'
    ),
    path(
        'delete/<pk>/',
        GaControlDeleteView.as_view(),
        name='ga_control_delete'
    ),
    path(
        'update/<pk>/',
        GaControlUpdateView.as_view(),
        name='ga_control_update'
    ),
    path(
        'create/<risk>/',
        GaControlCreateView.as_view(),
        name='ga_control_create'
    ),
    path(
        'create/',
        GaControlCreateView.as_view(),
        name='ga_control_create'
    ),
    path(
        'import/',
        GaControlImport.as_view(),
        name='ga_control_import'
    ),
]
