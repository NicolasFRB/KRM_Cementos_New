from krm.risks.api.risk_company_serializer import RiskCompanySerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from krm.questionnaires.models import QuestionTest


class QuestionTestApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un trío:
    - pk question_test
    - valor de respuesta
    - valor de descripción
    """

    def get(self, request):
        question_test_pk = int(request.GET['pk'])

        question_test = get_object_or_404(
            QuestionTest,
            pk=question_test_pk
        )

        if request.user != question_test.evaluator:
            data = {
                'status': 'ko',
                'text': 'No tienes permisos para evaluar esta pregunta'
            }

            return Response(data)

        if question_test.status == 1:
            if 'answer' in request.GET:
                answer = int(request.GET['answer'])
                if answer != 0:
                    question_test.answer = answer

            if 'description' in request.GET:
                description = request.GET['description']
                question_test.description = description

        question_test.save()

        data = {
            'status': 'ok'
        }

        return Response(data)
