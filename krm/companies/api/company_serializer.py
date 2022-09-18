from django.urls import path, include
from krm.users.models import User
from krm.companies.models import Company
from rest_framework import serializers, viewsets
from rest_framework.response import Response


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = [
            'pk',
            'name',
            'vat',
            'country',
            'email',
        ]
        read_only_fields = [f.name for f in Company._meta.get_fields()]


class CompanyViewSet(viewsets.ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def list(self, request):
        if 'user' in request.query_params:
            user = User.objects.get(pk=request.query_params['user'])
            if user.is_superuser:
                queryset = Company.objects.all()
            else:
                queryset = user.companies_admin.all()
        else:
            queryset = Company.objects.all()
        serializer = CompanySerializer(queryset, many=True)
        return Response(serializer.data)
