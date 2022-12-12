from django.urls import path, include

from rest_framework import serializers, viewsets
from rest_framework.response import Response
import django_filters.rest_framework


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from krm.questionnaires.models import Question


class QuestionSerializer(serializers.ModelSerializer):
    potential_users_to_assign = serializers.SerializerMethodField()
    scopes_names = serializers.SerializerMethodField()

    class Meta:
        model = Question
        fields = [
            'pk',
            'ref',
            'title',
            # 'questionnaires_pk',
            # 'user_to_assign',
            'potential_users_to_assign',
            'scopes_names',
        ]
        read_only_fields = [f.name for f in Question._meta.get_fields()]

    def get_potential_users_to_assign(self, obj):
        users = []
        for scope in obj.scopes.all():
            users = users + [{'value': int(user.pk), 'label': user.email}
                             for user in scope.user_to_assign.all()]
        return [dict(t) for t in {tuple(d.items()) for d in users}]

    def get_scopes_names(self, obj):
        return [scope.ref for scope in obj.scopes.all()]


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().distinct()
    serializer_class = QuestionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('scopes__questionnaire', )
