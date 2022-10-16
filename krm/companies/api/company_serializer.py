from django.urls import path, include
from krm.users.models import User
from krm.companies.models import Company
from rest_framework import serializers, viewsets
from rest_framework.response import Response


from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'pk',
            'name',
            'vat',
            'email',
        ]
        read_only_fields = [f.name for f in Company._meta.get_fields()]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        if request.user.is_superuser:
            queryset = Company.objects.all()
        else:
            queryset = request.user.companies_admin.all()

        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)
