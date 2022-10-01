from django.urls import path, include
from django.contrib.auth.models import User
from krm.risks.models import Risk, RiskCompany
from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class RiskCompanySerializer(serializers.ModelSerializer):

    class Meta:
        model = RiskCompany
        fields = [
            'pk',
            'company',
            'name',
            'description',
            'risk',
            'risk_ref',
            'active',
            'expert_assign',
            'expert_pk',
            'krm_activity_affected',
            'krm_main_events',
            'krm_exposed_staff',
            'krm_main_elements',
        ]
        read_only_fields = [f.name for f in Risk._meta.get_fields()]


class RiskCompanyViewSet(viewsets.ModelViewSet):
    queryset = RiskCompany.objects.all()
    serializer_class = RiskCompanySerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['ref', ]
