from django.urls import path, include

from rest_framework import serializers, viewsets
from rest_framework.response import Response


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from krm.questionnaires.models import Scope


class ScopeSerializer(serializers.ModelSerializer):
    user_to_assign_emails = serializers.SerializerMethodField()

    class Meta:
        model = Scope
        fields = [
            'pk',
            'ref',
            'name',
            'user_to_assign',
            'user_to_assign_emails'
        ]
        read_only_fields = [f.name for f in Scope._meta.get_fields()]

    def get_user_to_assign_emails(self, obj):
        return [{'value': int(user.pk), 'label': user.email} for user in obj.user_to_assign.all()]


class ScopeViewSet(viewsets.ModelViewSet):
    queryset = Scope.objects.all()
    serializer_class = ScopeSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
