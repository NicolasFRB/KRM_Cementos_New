from django.urls import path, include
from django.contrib.auth.models import User
from krm.risks.models import DomainRisk
from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class DomainRiskSerializer(serializers.ModelSerializer):

    class Meta:
        model = DomainRisk
        fields = [
            'pk',
            'ref',
            'name',
            'description',
        ]
        read_only_fields = [f.name for f in DomainRisk._meta.get_fields()]


class DomainRiskViewSet(viewsets.ModelViewSet):
    queryset = DomainRisk.objects.all()
    serializer_class = DomainRiskSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['ref', ]
