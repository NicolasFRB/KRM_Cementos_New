from django.urls import path, include
from django.contrib.auth.models import User
from krm.controls.models import Control
from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class ControlSerializer(serializers.ModelSerializer):
    risks = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    sub_processes = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    domain_risks = serializers.ListField(
        read_only=True
    )

    processes = serializers.ListField(
        read_only=True
    )

    class Meta:
        model = Control
        fields = [
            'pk',
            'ref',
            'name',
            'risks',
            'sub_processes',
            'domain_risks',
            'processes',
            'companies'
        ]
        read_only_fields = [f.name for f in Control._meta.get_fields()]


class ControlViewSet(viewsets.ModelViewSet):
    queryset = Control.objects.all()
    serializer_class = ControlSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
