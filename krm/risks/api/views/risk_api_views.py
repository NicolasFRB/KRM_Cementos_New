from krm.risks.api.risk_company_serializer import RiskCompanySerializer
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from krm.companies.models import(
    Company,
    CompanyDomainRiskEvaluator
)
from krm.risks.models import (
    Risk,
    RiskCompany
)
from krm.evaluations_krm.models import (
    EvaluationKrmInherent,
    RiskTestInherent
)
from krm.companies.api import CompanySerializer
from krm.risks.api import RiskSerializer
from krm.risks.models import RiskCompany


class RiskCompanyApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un listado de compañías y un listado de riesgos y devuelve el listado de riesgos compañías que le aplican a cada una """

    def get(self, request):
        company_pks = request.GET['company_pks'].split(',')
        risk_pks = request.GET['risk_pks'].split(',')

        data = []

        for c in Company.objects.filter(pk__in=(company_pks)):
            data_item = {}
            company = CompanySerializer(c)
            data_item['company'] = company.data
            data_item['risks'] = []
            for krm_risk in c.krm_risks.filter(risk__pk__in=(risk_pks), active=True).order_by('risk__ref'):
                data_item['risks'].append(RiskCompanySerializer(krm_risk).data)

            data.append(data_item)

        return Response(data)


class RiskCompanyResidualApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un listado de compañías y un listado de riesgos y devuelve el listado de riesgos compañías que le aplican a cada una y comprobando si se han lanzado test de control para alguna evaluación de su compañía"""

    def get(self, request):
        company_pks = request.GET['company_pks'].split(',')
        risk_pks = request.GET['risk_pks'].split(',')

        data = []

        for c in Company.objects.filter(pk__in=(company_pks)):
            data_item = {}
            company = CompanySerializer(c)
            data_item['company'] = company.data
            data_item['risks'] = []

            # Riesgos para los cuales se ha realizado un test de riesgo inherente de esa compañía
            risks_evaluated = RiskTestInherent.objects.filter(
                evaluation__in=EvaluationKrmInherent.objects.filter(company=c),
                status=3
            )

            for krm_risk in c.krm_risks.filter(risk__pk__in=(risk_pks), active=True).order_by('risk__ref'):
                # Ahora comprobamos si para este riesgo-compañía se han lanzado test de riesgo inherente
                risk = RiskCompanySerializer(krm_risk).data
                risk['evaluated'] = False
                risk['domain_risk_evaluator'] = []
                # if krm_risk in risks_evaluated:
                risk['evaluated'] = True
                company_domain_risk_evaluator = CompanyDomainRiskEvaluator.objects.get(
                    company=c,
                    domain_risk=krm_risk.risk.risk_master.domain_risk)
                risk['company_domain_risk_evaluator'] = company_domain_risk_evaluator.pk
                for evaluator in company_domain_risk_evaluator.evaluator.all():
                    risk['domain_risk_evaluator'].append(evaluator.email)

                data_item['risks'].append(risk)

            data.append(data_item)

        return Response(data)
