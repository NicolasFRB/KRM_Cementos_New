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
    RuEvaluationRiskInherentComplete,

    GaEvaluationResidualListView,
    GaEvaluationResidualCreateView,
    GaEvaluationResidualDetailView,
)

urlpatterns = [
    path(
        'inherent/',
        GaEvaluationInherentListView.as_view(),
        name='ga_evaluation_inherent_list'
    ),

    path(
        'inherent/create/',
        GaEvaluationInherentCreateView.as_view(),
        name='ga_evaluation_inherent_create'
    ),
    path(
        'detail/<pk>/',
        GaEvaluationInherentDetailView.as_view(),
        name='ga_evaluation_krm_inherent_detail'
    ),

    path(
        'ca/inherent/',
        CaEvaluationInherentListView.as_view(),
        name='ca_evaluation_inherent_list'
    ),

    path(
        'ca/inherent/create/',
        CaEvaluationInherentCreateView.as_view(),
        name='ca_evaluation_inherent_create'
    ),
    path(
        'ca/inherent/detail/<pk>/',
        CaEvaluationInherentDetailView.as_view(),
        name='ca_evaluation_inherent_detail'
    ),
    path(
        'ca/inherent/complete/<pk>/',
        CaEvaluationInherentAdminComplete.as_view(),
        name='ca_evaluation_inherent_complete'
    ),

    path(
        'ru/inherent/',
        RuEvaluationRiskInherentList.as_view(),
        name='ru_evaluation_risk_inherent_list'
    ),

    path(
        'ru/inherent/complete/<pk>/',
        RuEvaluationRiskInherentComplete.as_view(),
        name='ru_evaluation_risk_inherent_complete'
    ),



    path(
        'residual/',
        GaEvaluationResidualListView.as_view(),
        name='ga_evaluation_residual_list'
    ),
    path(
        'residual/create/',
        GaEvaluationResidualCreateView.as_view(),
        name='ga_evaluation_residual_create'
    ),
    path(
        'residual/detail/<pk>/',
        GaEvaluationResidualDetailView.as_view(),
        name='ga_evaluation_krm_residual_detail'
    ),
]
