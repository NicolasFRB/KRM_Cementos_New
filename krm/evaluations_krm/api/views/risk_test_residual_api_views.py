from krm.risks.api.risk_company_serializer import RiskCompanySerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from krm.evaluations_krm.models import RiskTestResidual


class RiskTestResidualEvaluatorApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un trío:
    - pk risk_test_inherent
    - valor de probabilidad
    - valor de impacto
    """

    def get(self, request):
        risk_test_pk = int(request.GET['pk'])

        risk_test = get_object_or_404(
            RiskTestResidual,
            pk=risk_test_pk
        )

        if risk_test.status == 1:
            if 'probability' in request.GET:
                probability = int(request.GET['probability'])
                if probability != 0:
                    risk_test.probability_level_residual_evaluator = probability

            if 'description' in request.GET:
                description = request.GET['description']
                risk_test.description_evaluator = description

        if risk_test.status == 2:

            if 'adminProbability' in request.GET:
                probability = int(request.GET['adminProbability'])
                if probability != 0:
                    risk_test.probability_level_administrator = probability

            if 'descriptionAdmin' in request.GET:
                description_admin = request.GET['descriptionAdmin']
                risk_test.description_administrator = description_admin

        risk_test.save()

        data = {
            'status': 'ok'
        }

        return Response(data)
