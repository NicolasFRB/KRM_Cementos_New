from django.urls import path, include
from django.contrib.auth.models import User
from krm.risks.models import Risk
from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class RiskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Risk
        fields = [
            'pk',
            'ref',
            'name',
            'description',
            'domain_risk',
            'impact_inherent',
            'probability_inherent',
            'impact_residual',
            'probability_residual',
        ]
        read_only_fields = [f.name for f in Risk._meta.get_fields()]


class RiskViewSet(viewsets.ModelViewSet):
    queryset = Risk.objects.all()
    serializer_class = RiskSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['ref', ]
