from krm.risks.api.risk_company_serializer import RiskCompanySerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from krm.evaluations_krm.models import RiskTestInherent


class RiskTestInherentExpertApiView(APIView):
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
            RiskTestInherent,
            pk=risk_test_pk
        )

        if 'probability' in request.GET:
            probability = int(request.GET['probability'])
            if probability != 0:
                risk_test.probability_level_expert = probability

        if 'impactEconomic' in request.GET:
            impact = int(request.GET['impactEconomic'])
            if impact != 0:
                risk_test.impact_economic_level_expert = impact

        if 'impactContinuity' in request.GET:
            impact = int(request.GET['impactContinuity'])
            if impact != 0:
                risk_test.impact_continuity_level_expert = impact

        if 'impactBranding' in request.GET:
            impact = int(request.GET['impactBranding'])
            if impact != 0:
                risk_test.impact_branding_level_expert = impact

        if 'adminProbability' in request.GET:
            probability = int(request.GET['adminProbability'])
            if probability != 0:
                risk_test.probability_level_administrator = probability

        if 'adminImpact' in request.GET:
            impact = int(request.GET['adminImpact'])
            if impact != 0:
                risk_test.impact_level_administrator = impact

        risk_test.save()

        data = {
            'status': 'ok'
        }

        return Response(data)
