from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.process.views import (
    GaProcessListView,
    GaProcessCreateView,
    GaProcessDeleteView,
    GaProcessDetailView,
    GaProcessUpdateView
)

urlpatterns = [
    path(
        '',
        GaProcessListView.as_view(),
        name='ga_process_list'
    ),
    path(
        'detail/<pk>/',
        GaProcessDetailView.as_view(),
        name='ga_process_detail'
    ),
    path(
        'delete/<pk>/',
        GaProcessDeleteView.as_view(),
        name='ga_process_delete'
    ),
    path(
        'update/<pk>/',
        GaProcessUpdateView.as_view(),
        name='ga_process_update'
    ),
    path(
        'create/',
        GaProcessCreateView.as_view(),
        name='ga_process_create'
    ),
]
