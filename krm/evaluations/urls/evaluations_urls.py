from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.evaluations.views import (
    GaEvaluationListView,
    GaEvaluationCreateView,
    GaEvaluationDetailView,
    GaEvaluationUpdateView,
    GaEvaluationDeleteView,
    GaEvaluationNotificationView,
    EvaluationAssignImport,

    CaEvaluationListView,
    CaEvaluationCreateView,
    CaEvaluationDetailView,
    CaEvaluationUpdateView,
    CaEvaluationDeleteView,
    CaEvaluationAssignImport,
    CaEvaluationNotificationView,

    AuEvaluationListView,
    AuEvaluationDetailView
)

urlpatterns = [
    path(
        'detail/<pk>/',
        GaEvaluationDetailView.as_view(),
        name='ga_evaluation_detail'
    ),
    path(
        'update/<pk>/',
        GaEvaluationUpdateView.as_view(),
        name='ga_evaluation_update'
    ),
    path(
        'delete/<pk>/',
        GaEvaluationDeleteView.as_view(),
        name='ga_evaluation_delete'
    ),
    path(
        '',
        GaEvaluationListView.as_view(),
        name='ga_evaluation_list'
    ),
    path(
        'create/',
        GaEvaluationCreateView.as_view(),
        name='ga_evaluation_create'
    ),
    path(
        'notifications/<pk>/',
        GaEvaluationNotificationView.as_view(),
        name='ga_evaluation_notifications'
    ),
    path(
        "assign-control-import/<pk>/",
        EvaluationAssignImport.as_view(),
        name="ga_evaluation_import_assign_control",
    ),

    path(
        'ca/detail/<pk>/',
        CaEvaluationDetailView.as_view(),
        name='ca_evaluation_detail'
    ),
    path(
        'ca/update/<pk>/',
        CaEvaluationUpdateView.as_view(),
        name='ca_evaluation_update'
    ),
    path(
        'ca/delete/<pk>/',
        CaEvaluationDeleteView.as_view(),
        name='ca_evaluation_delete'
    ),
    path(
        'ca/',
        CaEvaluationListView.as_view(),
        name='ca_evaluation_list'
    ),
    path(
        'ca/create/',
        CaEvaluationCreateView.as_view(),
        name='ca_evaluation_create'
    ),
    path(
        "ca/assign-control-import/<pk>/",
        CaEvaluationAssignImport.as_view(),
        name="ca_evaluation_import_assign_control",
    ),

    path(
        'auditor/evaluations-krc/',
        AuEvaluationListView.as_view(),
        name='au_evaluation_list'
    ),
    path(
        'auditor/evaluations-krc/<pk>/',
        AuEvaluationDetailView.as_view(),
        name='au_evaluation_detail'
    ),

    path(
        'ca/notifications/<pk>/',
        CaEvaluationNotificationView.as_view(),
        name='ca_evaluation_notifications'
    ),
]
