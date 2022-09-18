from django.urls import path, include
from django.contrib.auth.models import User
from krm.process.models import Process
from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend


class ProcessSerializer(serializers.ModelSerializer):
    sub_processes = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True
    )

    class Meta:
        model = Process
        fields = [
            'pk',
            'ref',
            'name',
            'description',
            'sub_processes',
        ]
        read_only_fields = [f.name for f in Process._meta.get_fields()]


class ProcessViewSet(viewsets.ModelViewSet):
    queryset = Process.objects.all()
    serializer_class = ProcessSerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['ref', ]
