from krm.risks.api.risk_company_serializer import RiskCompanySerializer
from krm.risks.api.domain_risk_serializer import  DomainRiskSerializer
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
from krm.users.models import (
    User
)

from krm.evaluations_krm.models import (
    EvaluationKrmInherent,
    RiskTestInherent
)
from krm.companies.api import CompanySerializer
from krm.risks.api import RiskSerializer
from krm.risks.models import RiskCompany

from krm.users.api import UserSerializer

from django.http import HttpResponse



class RiskDomainRiskApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un listado de compañías y devuelve el listado de dominios de riesgos que le aplican a cada una de las compañias"""

    def get(self, request):
        company_pks = request.GET['company_pks'].split(',')
        domain_risk_pks = request.GET['domain_risk_pks'].split(',')
        # risk_pks = request.GET['risk_pks'].split(',')
        domain_risk_pks = list(filter(None, domain_risk_pks))
        data = []


        for c in Company.objects.filter(pk__in=(company_pks)):
            data_item = {}
            data_item['company'] = CompanySerializer(c).data
            data_item['risks'] = []
            all_risks = c.krm_risks_active.all()

            print("DOmain risks pks")
            print(domain_risk_pks)

            for risk in all_risks:
                print(risk.risk.risk_master)
                if len(domain_risk_pks) == 0 or str(risk.risk.risk_master.domain_risk.pk) in domain_risk_pks:            
                    data_item['risks'].append(RiskSerializer(risk.risk).data)
            data.append(data_item)

        return Response(data)
    
class DomainRiskCompanyApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un listado de compañías y devuelve el listado de dominios de riesgos que le aplican a cada una de las compañias"""

    def get(self, request):
        company_pks = request.GET['company_pks'].split(',')
        # risk_pks = request.GET['risk_pks'].split(',')

        data = []

        for c in Company.objects.filter(pk__in=(company_pks)):
            data_item = {}
            company = CompanySerializer(c)
            data_item['company'] = company.data
            data_item['domain_risks'] = []

            for risk in c.krm_risks_active.all():
                data_item['domain_risks'].append(DomainRiskSerializer(risk.risk.risk_master.domain_risk).data)

            data.append(data_item)

        return Response(data)
    
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
            
            # for employee in c.employees.all():
            #     data_item['company']['employees'].append(UserSerializer(employee).data)
                
            
            data_item['risks'] = []
            
            
            for krm_risk in c.krm_risks.filter(risk__pk__in=(risk_pks), active=True).order_by('risk__ref'):
                # Por algun motivo los riesgos de la segunda compañia no aparecen
                print(krm_risk.risk.name) 
                risk = RiskCompanySerializer(krm_risk).data

                if risk["expert"]:
                    risk["expert_data"] = UserSerializer(User.objects.get(pk=risk["expert"])).data
                
                if risk["evaluator"]:
                    risk["evaluator_data"] = UserSerializer(User.objects.get(pk=risk["evaluator"])).data

                data_item['risks'].append(risk)

            data.append(data_item)

        return Response(data)


class RiskCompanyResidualApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un listado de compañías y un listado de riesgos y devuelve el listado de riesgos compañías que le aplican a cada una y comprobando si se han lanzado test de riesgo inherente para alguna evaluación de su compañía"""

    def get(self, request):
        company_pks = request.GET['company_pks'].split(',')
        risk_pks = request.GET['risk_pks'].split(',')

        data = []

        for c in Company.objects.filter(pk__in=(company_pks)):
            data_item = {}
            company = CompanySerializer(c)
            data_item['company'] = company.data
            data_item['risks'] = []

            # Riesgos compañía para los cuales se ha realizado un test de riesgo inherente de esa compañía
            risks_evaluated = [rt.risk for rt in RiskTestInherent.objects.filter(
                evaluation__in=EvaluationKrmInherent.objects.filter(company=c),
                status=3
            )]

            for krm_risk in c.krm_risks.filter(risk__pk__in=(risk_pks), active=True).order_by('risk__ref'):
                # Ahora comprobamos si para este riesgo-compañía se han lanzado test de riesgo inherente
                risk = RiskCompanySerializer(krm_risk).data
                risk['evaluated'] = False
                risk['latest_inherent_impact_level_admin'] = 0
                risk['latest_inherent_probability_level_admin'] = 0
                risk['domain_risk_evaluator'] = []

                if krm_risk in risks_evaluated:
                    risk['evaluated'] = True
                    last_evaluate_risk_inherent = krm_risk.risk_test.filter(
                        status=3,
                        evaluation__status='FI'
                    ).order_by('evaluation__date_begin').first()
                    risk['severity_level_expert_qualitative'] = last_evaluate_risk_inherent.severity_level_expert_qualitative
                    risk['severity_level_admin_qualitative'] = last_evaluate_risk_inherent.severity_level_admin_qualitative

                company_domain_risk_evaluator = CompanyDomainRiskEvaluator.objects.get(
                    company=c,
                    domain_risk=krm_risk.risk.risk_master.domain_risk)
                risk['company_domain_risk_evaluator'] = company_domain_risk_evaluator.pk
                for evaluator in company_domain_risk_evaluator.evaluator.all():
                    risk['domain_risk_evaluator'].append(evaluator.email)

                data_item['risks'].append(risk)

            data.append(data_item)

        return Response(data)

class RiskCompanyExpertApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, request, *args, **kwargs):
        company_risks = request.POST.get('company_risks')

        print(company_risks)

        # self.company.krm_risks.filter(
        #     pk__in=risk_company_selected).update(active=True)
        # self.company.krm_risks.exclude(
        #     pk__in=risk_company_selected).update(active=False)

        # messages.add_message(
        #     self.request, messages.SUCCESS, _(
        #         "Riesgos (N2) que aplican sobre %s actualizados correctamente" % self.company.name)
        # )

        return HttpResponse(status=200)
