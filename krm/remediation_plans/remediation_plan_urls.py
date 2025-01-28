from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.remediation_plans.views import (
    GaRemediationPlanListView,
    GaRemediationPlanCreateView,
    GaRemediationPlanCreateSelectCompanyView,
    GaRemediationPlanDeleteView,
    GaRemediationPlanDetailView,
    GaRemediationPlanUpdateView,
    delete_attachment,

    RuRemediationPlanListView,
    RuRemediationPlanDetailView,

    AuRemediationPlanListView,
    AuRemediationPlanDetailView
)


urlpatterns = [
    path(
        '',
        GaRemediationPlanListView.as_view(),
        name='ga_remediation_plan_list'
    ),
    path(
        'detail/<pk>/',
        GaRemediationPlanDetailView.as_view(),
        name='ga_remediation_plan_detail'
    ),
    path(
        'delete/<pk>/',
        GaRemediationPlanDeleteView.as_view(),
        name='ga_remediation_plan_delete'
    ),
    path(
        'update/<pk>/',
        GaRemediationPlanUpdateView.as_view(),
        name='ga_remediation_plan_update'
    ),
    path(
        'create/select-company/',
        GaRemediationPlanCreateSelectCompanyView.as_view(),
        name='ga_remediation_plan_create_select_company'
    ),
    path(
        'create/<company_pk>/',
        GaRemediationPlanCreateView.as_view(),
        name='ga_remediation_plan_create'
    ),
    path(
        "delete-attachment/<pk_remediation_plan>/<pk_attachment>/",
        delete_attachment,
        name='delete_attachment'
    ),
    path(
        'ru/list/',
        RuRemediationPlanListView.as_view(),
        name='ru_remediation_plan_list'
    ),

    path(
        'ru/detail/<pk>',
        RuRemediationPlanDetailView.as_view(),
        name='ru_remediation_plan_detail'
    ),

    path(
        'au/list/',
        AuRemediationPlanListView.as_view(),
        name='au_remediation_plan_list'
    ),

    path(
        'au/detail/<pk>',
        AuRemediationPlanDetailView.as_view(),
        name='au_remediation_plan_detail'
    ),
]
