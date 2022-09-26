from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.risks.views import (
    RiskCompanyUpdateView,
    CaRiskCompanyUpdateView
)

urlpatterns = [
    path(
        'update/<pk>/',
        RiskCompanyUpdateView.as_view(),
        name='ga_risk_company_update'
    ),
    path(
        'ca/update/<pk>/',
        CaRiskCompanyUpdateView.as_view(),
        name='ca_risk_company_update'
    ),
]
