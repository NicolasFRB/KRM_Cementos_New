from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.risks.views import (
    GaRiskListView,
    GaRiskCreateView,
    GaRiskDeleteView,
    GaRiskDetailView,
    GaRiskUpdateView
)

urlpatterns = [
    path(
        '',
        GaRiskListView.as_view(),
        name='ga_risk_list'
    ),
    path(
        'detail/<pk>/',
        GaRiskDetailView.as_view(),
        name='ga_risk_detail'
    ),
    path(
        'delete/<pk>/',
        GaRiskDeleteView.as_view(),
        name='ga_risk_delete'
    ),
    path(
        'update/<pk>/',
        GaRiskUpdateView.as_view(),
        name='ga_risk_update'
    ),
    path(
        'create/<risk>/',
        GaRiskCreateView.as_view(),
        name='ga_risk_create'
    ),
    path(
        'create/',
        GaRiskCreateView.as_view(),
        name='ga_risk_create'
    ),
]
