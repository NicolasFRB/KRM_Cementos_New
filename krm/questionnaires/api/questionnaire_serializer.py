from django.urls import path, include

from rest_framework import serializers, viewsets
from rest_framework.response import Response


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from krm.questionnaires.models import Questionnaire


class QuestionnaireSerializer(serializers.ModelSerializer):
    scopes_names = serializers.SerializerMethodField()

    class Meta:
        model = Questionnaire
        fields = [
            'pk',
            'name',
            'scopes_names',
        ]

    def get_scopes_names(self, obj):
        return [{'value': int(scope.pk), 'label': scope.ref} for scope in obj.scopes.all()]


class QuestionnaireViewSet(viewsets.ModelViewSet):
    queryset = Questionnaire.objects.all()
    serializer_class = QuestionnaireSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
