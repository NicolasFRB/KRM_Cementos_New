from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.risks.views import (
    GaRiskMasterListView,
    GaRiskMasterCreateView,
    GaRiskMasterDetailView,
    GaRiskMasterUpdateView,
    GaRiskMasterDeleteView
)

urlpatterns = [
    path(
        'detail/<pk>/',
        GaRiskMasterDetailView.as_view(),
        name='ga_risk_master_detail'
    ),
    path(
        'update/<pk>/',
        GaRiskMasterUpdateView.as_view(),
        name='ga_risk_master_update'
    ),
    path(
        'delete/<pk>/',
        GaRiskMasterDeleteView.as_view(),
        name='ga_risk_master_delete'
    ),
    path(
        '',
        GaRiskMasterListView.as_view(),
        name='ga_risk_master_list'
    ),
    path(
        'create/<domain_risk>/',
        GaRiskMasterCreateView.as_view(),
        name='ga_risk_master_create'
    ),
    path(
        'create/',
        GaRiskMasterCreateView.as_view(),
        name='ga_risk_master_create'
    ),
]
