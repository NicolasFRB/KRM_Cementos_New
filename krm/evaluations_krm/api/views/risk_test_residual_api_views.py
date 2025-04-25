from krm.risks.api.risk_company_serializer import RiskCompanySerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from krm.evaluations_krm.models import RiskTestResidual
#RiskCompanyResidual


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
                    risk_test.probability_level_evaluator = probability

            if 'impactReputational' in request.GET:
                impact = int(request.GET['impactReputational'])
                if impact != 0:
                    risk_test.impact_reputational_evaluator = impact

            if 'impactEconomic' in request.GET:
                impact = int(request.GET['impactEconomic'])
                if impact != 0:
                    risk_test.impact_economic_evaluator = impact

            if 'impactRegulatory' in request.GET:
                impact = int(request.GET['impactRegulatory'])
                if impact != 0:
                    risk_test.impact_regulatory_evaluator = impact

            if 'impactObjectives' in request.GET:
                impact = int(request.GET['impactObjectives'])
                if impact != 0:
                    risk_test.impact_objectives_evaluator = impact

            if 'impactDedication' in request.GET:
                impact = int(request.GET['impactDedication'])
                if impact != 0:
                    risk_test.impact_dedication_evaluator = impact

            if 'eventSpeed' in request.GET:
                speed= int(request.GET['eventSpeed'])
                if speed!=0:
                    risk_test.event_speed_level_evaluator= speed

            if 'description' in request.GET:
                description = request.GET['description']
                risk_test.description_evaluator = description

        # if risk_test.status == 2:

        if 'adminProbability' in request.GET:
            probability = int(request.GET['adminProbability'])
            if probability != 0:
                risk_test.probability_level_administrator = probability

        if 'adminImpact' in request.GET:
            impact = int(request.GET['adminImpact'])
            if impact != 0:
                risk_test.impact_level_administrator = impact

        if 'adminEventSpeed' in request.GET:
            speed= int(request.GET['adminEventSpeed'])
            if speed!=0:
                risk_test.event_speed_level_administrator= speed

        if 'descriptionAdmin' in request.GET:
            description_admin = request.GET['descriptionAdmin']
            risk_test.description_administrator = description_admin

        print(risk_test.probability_level_administrator)
        print(risk_test.impact_level_administrator)
        print(risk_test.event_speed_level_administrator)
        print(risk_test.description_administrator)
        risk_test.save()

        data = {
            'status': 'ok'
        }

        return Response(data)


# class RiskCompanyResidualAdminApiView(APIView):
#     authentication_classes = [SessionAuthentication, BasicAuthentication]
#     permission_classes = [IsAuthenticated]
#     """ Función que recibe un trío:
#     - pk risk_test_inherent
#     - valor de probabilidad
#     - valor de impacto
#     """

#     def get(self, request):
#         risk_test_pk = int(request.GET['pk'])

#         risk_company_residual = get_object_or_404(
#             RiskCompanyResidual,
#             pk=risk_test_pk
#         )

#         if 'adminProbability' in request.GET:
#             probability = int(request.GET['adminProbability'])
#             if probability != 0:
#                 risk_company_residual.probability_level_residual_administrator = probability

#         if 'descriptionAdmin' in request.GET:
#             description_admin = request.GET['descriptionAdmin']
#             risk_company_residual.description_administrator = description_admin

#         risk_company_residual.save()

#         data = {
#             'status': 'ok'
#         }

#         return Response(data)
