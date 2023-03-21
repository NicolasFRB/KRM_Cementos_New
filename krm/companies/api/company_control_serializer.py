from django.urls import path, include
from django.contrib.auth.models import User
from krm.controls.models import Control
from rest_framework import routers, serializers, viewsets
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


from krm.companies.models import CompanyControls
from krm.users.api import UserSerializer
from krm.controls.api import ControlSerializer


class CompanyControlSerializer(serializers.ModelSerializer):
    control = ControlSerializer(
        read_only=True
    )

    control_test_owners = UserSerializer(
        many=True,
        read_only=True
    )

    control_test_supervisors = UserSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = CompanyControls
        fields = [
            'pk',
            'active',
            'company',
            'control',
            'control_test_owners',
            'control_test_supervisors'
        ]
        read_only_fields = [f.name for f in Control._meta.get_fields()]


class CompanyControlViewSet(viewsets.ModelViewSet):
    queryset = CompanyControls.objects.all()
    serializer_class = CompanyControlSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]


# // http:/ localhost: 8000/api/controlscompany /?company_pks = 21 & risk_pks = &elc = false & key_control = false & process_pks = &domain_risk_pks =

# # [
#     {
#         "c": {
#             "pk": 21,
#             "name": "Baética Digital",
#             "vat": null,
#             "email": null
#         },
#         "cs": [
#             {
#                 "pk": 2,
#                 "active": true,
#                 "company": 21,
#                 "control": 976,
#                 "control_test_owners": [
#                     {
#                         "pk": 98,
#                         "email": "39@39.com",
#                         "full_name": "Mario Ar"
#                     },
#                     {
#                         "pk": 107,
#                         "email": "ru@baetica.com",
#                         "full_name": "ru@baetica.com "
#                     },
#                     {
#                         "pk": 106,
#                         "email": "bienvenidosaez@baetica.com",
#                         "full_name": "Bienvenido Sáez Muelas"
#                     }
#                 ],
#                 "control_test_supervisors": [
#                     {
#                         "pk": 105,
#                         "email": "mrevuelta.deca@gmail.com",
#                         "full_name": "asd asd"
#                     }
#                 ]
#             },
#             {
#                 "pk": 2942,
#                 "active": true,
#                 "company": 21,
#                 "control": 976,
#                 "control_test_owners": [
#                     {
#                         "pk": 107,
#                         "email": "ru@baetica.com",
#                         "full_name": "ru@baetica.com "
#                     },
#                     {
#                         "pk": 1,
#                         "email": "marioalvarez1@kpmg.es",
#                         "full_name": "Mario Alvarez"
#                     }
#                 ],
#                 "control_test_supervisors": [
#                     {
#                         "pk": 18,
#                         "email": "prueba@prueba.com",
#                         "full_name": "Mario Ar"
#                     }
#                 ]
#             },
#             {
#                 "pk": 2943,
#                 "active": true,
#                 "company": 21,
#                 "control": 977,
#                 "control_test_owners": [

#                 ],
#                 "control_test_supervisors": [

#                 ]
#             },
#             {
#                 "pk": 2944,
#                 "active": true,
#                 "company": 21,
#                 "control": 978,
#                 "control_test_owners": [
#                     {
#                         "pk": 18,
#                         "email": "prueba@prueba.com",
#                         "full_name": "Mario Ar"
#                     },
#                     {
#                         "pk": 106,
#                         "email": "bienvenidosaez@baetica.com",
#                         "full_name": "Bienvenido Sáez Muelas"
#                     }
#                 ],
#                 "control_test_supervisors": [
#                     {
#                         "pk": 18,
#                         "email": "prueba@prueba.com",
#                         "full_name": "Mario Ar"
#                     },
#                     {
#                         "pk": 1,
#                         "email": "marioalvarez1@kpmg.es",
#                         "full_name": "Mario Alvarez"
#                     }
#                 ]
#             }
#         ]
#     }
# ]
