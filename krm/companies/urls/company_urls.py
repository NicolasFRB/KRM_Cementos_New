from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.cache import cache_page

from krm.companies.views import (
    GaCompanyListView,
    GaCompanyCreateView,
    GaCompanyDeleteView,
    GaCompanyDetailView,
    GaCompanyUpdateView,
    GaCompanyImportView,

    GaCompanyDomainRiskExpertsUpdateView,
    GaCompanyRiskKrmSelectView,
    GaCompanyDomainRiskEvaluatorUpdateView,

    CaCompanyDetailView,
    CaCompanyListView,
    CaCompanyUpdateView,
    CaCompanyRiskKrmSelectView,
    CaCompanyDomainRiskExpertsUpdateView,
    CaCompanyDomainRiskEvaluatorUpdateView
)


urlpatterns = [
    path(
        '',
        cache_page(60*60)(GaCompanyListView.as_view()),
        name='ga_company_list'
    ),
    path(
        'import/',
        GaCompanyImportView.as_view(),
        name='ga_company_import'
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

    path(
        'assign-expert/<pk>/',
        GaCompanyDomainRiskExpertsUpdateView.as_view(),
        name='ga_company_assign_expert_update'
    ),

    path(
        'assign-evaluator/<pk>/',
        GaCompanyDomainRiskEvaluatorUpdateView.as_view(),
        name='ga_company_assign_evaluator_update'
    ),

    path(
        'krm-risk-select/<pk>/',
        GaCompanyRiskKrmSelectView.as_view(),
        name='ga_company_risk_krm_select'
    ),


    path(
        'ca/',
        CaCompanyListView.as_view(),
        name='ca_company_list'
    ),
    path(
        'ca/detail/<pk>/',
        CaCompanyDetailView.as_view(),
        name='ca_company_detail'
    ),
    path(
        'ca/update/<pk>/',
        CaCompanyUpdateView.as_view(),
        name='ca_company_update'
    ),
    path(
        'ca/krm-risk-select/<pk>/',
        CaCompanyRiskKrmSelectView.as_view(),
        name='ca_company_risk_krm_select'
    ),
    path(
        'ca/assign-expert/<pk>/',
        CaCompanyDomainRiskExpertsUpdateView.as_view(),
        name='ca_company_assign_expert_update'
    ),
    path(
        'ca/assign-evaluator/<pk>/',
        CaCompanyDomainRiskEvaluatorUpdateView.as_view(),
        name='ca_company_assign_evaluator_update'
    ),
]
