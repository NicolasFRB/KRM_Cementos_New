from django.urls import include, path, re_path
from django.views.decorators.csrf import csrf_exempt

from krm.risks.views import (
    GaDomainRiskListView,
    GaDomainRiskCreateView,
    GaDomainRiskDetailView,
    GaDomainRiskUpdateView
)

urlpatterns = [
    path(
        'detail/<pk>/',
        GaDomainRiskDetailView.as_view(),
        name='ga_domain_risk_detail'
    ),
    path(
        'update/<pk>/',
        GaDomainRiskUpdateView.as_view(),
        name='ga_domain_risk_update'
    ),
    path(
        '',
        GaDomainRiskListView.as_view(),
        name='ga_domain_risk_list'
    ),
    path(
        'create/',
        GaDomainRiskCreateView.as_view(),
        name='ga_domain_risk_create'
    ),
]
