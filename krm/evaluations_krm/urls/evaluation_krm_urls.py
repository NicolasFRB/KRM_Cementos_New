from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.evaluations_krm.views import (
    GaEvaluationKrmInherentCreateView,
    GaEvaluationKrmListView,
)

urlpatterns = [
    path(
        'krm/',
        GaEvaluationKrmListView.as_view(),
        name='ga_evaluation_krm_list'
    ),

    path(
        'krm/create/',
        GaEvaluationKrmInherentCreateView.as_view(),
        name='ga_evaluation_krm_inherent_create'
    ),

]
