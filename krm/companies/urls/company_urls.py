from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.companies.views import (
    GaCompanyListView,
    GaCompanyCreateView,
    GaCompanyDeleteView,
    GaCompanyDetailView,
    GaCompanyUpdateView
)

urlpatterns = [
    path(
        '',
        GaCompanyListView.as_view(),
        name='ga_company_list'
    ),
    path(
        'detail/<pk>/',
        GaCompanyDetailView.as_view(),
        name='ga_company_detail'
    ),
    path(
        'delete/<pk>/',
        GaCompanyDeleteView.as_view(),
        name='ga_company_delete'
    ),
    path(
        'update/<pk>/',
        GaCompanyUpdateView.as_view(),
        name='ga_company_update'
    ),
    path(
        'create/',
        GaCompanyCreateView.as_view(),
        name='ga_company_create'
    ),
]
