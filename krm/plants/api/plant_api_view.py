from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q

from krm.companies.models import Company
from krm.controls.models import Control

from krm.process.models import SubProcess

from krm.companies.api import CompanySerializer, CompanyControlSerializer
from krm.controls.api import ControlSerializer
import numpy as np

from krm.controls.models import FREQUENCY_CONTROL_CHOICES

class PlantApiView(APIView):
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    """ Función que recibe un listado de compañías y un listado de riesgos y devuelve el listado de riesgos compañías que le aplican a cada una """

    def get(self, request):

        plants = Control.objects.order_by().values_list('plant').distinct()

        data = [] 
        data.append(list(plants))

        return Response(np.array(plants).flatten())