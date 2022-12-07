from django.urls import path, include

from rest_framework import serializers, viewsets
from rest_framework.response import Response
import django_filters.rest_framework


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from krm.questionnaires.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    user_to_assign_emails = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'pk',
            'ref',
            'order',
            'title',
            'questionnaire',
            'user_to_assign',
            'user_to_assign_emails'
        ]
        read_only_fields = [f.name for f in Question._meta.get_fields()]

    def get_user_to_assign_emails(self, obj):
        return [{'value': int(user.pk), 'label': user.email} for user in obj.user_to_assign.all()]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('questionnaire', )
