from django.urls import path, include
from django.contrib.auth.models import User
from krm.controls.models import Control
from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from krm.companies.models import CompanyControls
from krm.users.api import UserSerializer
from krm.controls.api import ControlSerializer


class CompanyControlSerializer(serializers.ModelSerializer):
    control = ControlSerializer(
        read_only=True
    )

    control_test_owners = UserSerializer(
        many=True,
        read_only=True
    )

    control_test_supervisors = UserSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = CompanyControls
        fields = [
            'pk',
            'active',
            'company',
            'control',
            'control_test_owners',
            'control_test_supervisors'
        ]
        read_only_fields = [f.name for f in Control._meta.get_fields()]


class CompanyControlViewSet(viewsets.ModelViewSet):
    queryset = CompanyControls.objects.all()
    serializer_class = CompanyControlSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
