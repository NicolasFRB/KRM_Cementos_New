from django.urls import path, include
from django.contrib.auth.models import User
from krm.process.models import SubProcess

from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class SubProcessSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SubProcess
        fields = [
            'ref',
            'name',
            'description',
            'controls'
        ]
        read_only_fields = [f.name for f in SubProcess._meta.get_fields()]


class SubProcessViewSet(viewsets.ModelViewSet):
    queryset = SubProcess.objects.all()
    serializer_class = SubProcessSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
