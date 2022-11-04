from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from krm.companies.models import Company
from krm.controls.models import Control

from krm.process.models import SubProcess

from krm.companies.api import CompanySerializer
from krm.controls.api import ControlSerializer


class ControlCompanyApiView(APIView):
    """
      Vista encargada de recibir:
       - Lista de pk de compañías
       - Lista de dominios de riesgo
       - Lista de procesos
       - Lista de pk de riesgos

       Devuelve:
       - Lista de compañías con los controles asociados como hijos de la forma
    """
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        company_pks = []
        domain_risk_pks = []
        process_pks = []
        # risk_pks = []
        key_control = False
        elc = False

        if 'company_pks' in request.GET:
            if request.GET['company_pks']:
                company_pks = request.GET['company_pks'].split(',')
        if 'domain_risk_pks' in request.GET:
            if request.GET['domain_risk_pks']:
                domain_risk_pks = request.GET['domain_risk_pks'].split(',')
        if 'process_pks' in request.GET:
            if request.GET['process_pks']:
                process_pks = request.GET['process_pks'].split(',')
        # if 'risk_pks' in request.GET:
        #     risk_pks = request.GET['risk_pks'].split(',')
        if 'key_control' in request.GET:
            if request.GET['key_control'] == 'true':
                key_control = True
        if 'elc' in request.GET:
            if request.GET['elc'] == 'true':
                elc = True

        data = []

        for c in Company.objects.filter(pk__in=(company_pks)):
            data_item = {}
            company = CompanySerializer(c)
            data_item['c'] = company.data
            data_item['cs'] = []
            control_list = c.controls.all()

            # Ahora cada control hay que serializarlo
            if domain_risk_pks:
                control_list = control_list.filter(
                    risks__risk_master__domain_risk__pk__in=(domain_risk_pks)
                )

            # if risk_pks:
            #     control_list = control_list.filter(risks__pk__in=(risk_pks)
            #                                        )

            if process_pks:
                sub_processes = SubProcess.objects.filter(
                    process__pk__in=(process_pks)).values_list('id', flat=True)

                control_list = control_list.filter(
                    sub_processes__in=sub_processes
                )

            if key_control:
                control_list = control_list.filter(
                    key_control=True
                )

            if elc:
                # Si está marcado hay que añadirle todos los controles ELC que tenga la compañía cumpla o no los filtros anteriories
                control_list_elc = c.controls.filter(is_elc=True)
                control_list = control_list | control_list_elc

            control_list = control_list.distinct()

            for control in control_list:
                control_serializer = ControlSerializer(control)
                data_item['cs'].append(control_serializer.data)

            data.append(data_item)

        return Response(data)
