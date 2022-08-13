from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.risks.views import (
    GaRiskMasterListView,
    GaRiskMasterCreateView,
    GaRiskMasterDetailView,
    GaRiskMasterUpdateView
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
        '',
        GaRiskMasterListView.as_view(),
        name='ga_risk_master_list'
    ),
    path(
        'create/',
        GaRiskMasterCreateView.as_view(),
        name='ga_risk_master_create'
    ),
]
