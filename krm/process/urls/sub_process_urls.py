from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.process.views import (
    GaSubProcessListView,
    GaSubProcessCreateView,
    GaSubProcessDeleteView,
    GaSubProcessDetailView,
    GaSubProcessUpdateView
)

urlpatterns = [
    path(
        '',
        GaSubProcessListView.as_view(),
        name='ga_sub_process_list'
    ),
    path(
        'detail/<pk>/',
        GaSubProcessDetailView.as_view(),
        name='ga_sub_process_detail'
    ),
    path(
        'delete/<pk>/',
        GaSubProcessDeleteView.as_view(),
        name='ga_sub_process_delete'
    ),
    path(
        'update/<pk>/',
        GaSubProcessUpdateView.as_view(),
        name='ga_sub_process_update'
    ),
    path(
        'create/<process>/',
        GaSubProcessCreateView.as_view(),
        name='ga_sub_process_create'
    ),
    path(
        'create/',
        GaSubProcessCreateView.as_view(),
        name='ga_sub_process_create'
    ),
]
