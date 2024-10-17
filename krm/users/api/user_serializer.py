from django.urls import path, include

from rest_framework import serializers, viewsets
from rest_framework.response import Response
import django_filters.rest_framework


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from krm.users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'pk',
            'email',
            'full_name'
        ]


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True).order_by('email')
    serializer_class = UserSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
