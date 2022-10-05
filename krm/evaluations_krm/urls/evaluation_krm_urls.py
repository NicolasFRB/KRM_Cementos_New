from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt
from krm.evaluations.views.ga_evaluation_views import GaEvaluationDetailView

from krm.evaluations_krm.views import (
    GaEvaluationInherentCreateView,
    GaEvaluationInherentListView,
    GaEvaluationInherentDetailView,

    CaEvaluationInherentCreateView,
    CaEvaluationInherentListView,
    CaEvaluationInherentDetailView,
    CaEvaluationInherentAdminComplete,

    RuEvaluationRiskInherentList,
    RuEvaluationRiskInherentComplete
)

urlpatterns = [
    path(
        '',
        GaEvaluationInherentListView.as_view(),
        name='ga_evaluation_krm_list'
    ),

    path(
        'create/',
        GaEvaluationInherentCreateView.as_view(),
        name='ga_evaluation_inherent_create'
    ),
    path(
        'detail/<pk>/',
        GaEvaluationInherentDetailView.as_view(),
        name='ga_evaluation_krm_inherent_detail'
    ),

    path(
        'ca/',
        CaEvaluationInherentListView.as_view(),
        name='ca_evaluation_inherent_list'
    ),

    path(
        'ca/create/',
        CaEvaluationInherentCreateView.as_view(),
        name='ca_evaluation_inherent_create'
    ),
    path(
        'ca/detail/<pk>/',
        CaEvaluationInherentDetailView.as_view(),
        name='ca_evaluation_inherent_detail'
    ),
    path(
        'ca/complete/<pk>/',
        CaEvaluationInherentAdminComplete.as_view(),
        name='ca_evaluation_inherent_complete'
    ),

    path(
        'ru/',
        RuEvaluationRiskInherentList.as_view(),
        name='ru_evaluation_risk_inherent_list'
    ),

    path(
        'ru/complete/<pk>/',
        RuEvaluationRiskInherentComplete.as_view(),
        name='ru_evaluation_risk_inherent_complete'
    ),
]
