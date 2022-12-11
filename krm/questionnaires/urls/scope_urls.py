from django.urls import path

from krm.questionnaires.views import (
    GaScopeDetailView,
    GaScopeDeleteView,
    GaScopeUpdateView,
    GaScopeCreateView,
)


urlpatterns = [
    path(
        'detail/<pk>/',
        GaScopeDetailView.as_view(),
        name='ga_scope_detail'
    ),
    path(
        'delete/<pk>/',
        GaScopeDeleteView.as_view(),
        name='ga_scope_delete'
    ),
    path(
        'update/<pk>/',
        GaScopeUpdateView.as_view(),
        name='ga_scope_update'
    ),
    path(
        'create/<questionnaire>/',
        GaScopeCreateView.as_view(),
        name='ga_scope_create'
    ),
]
