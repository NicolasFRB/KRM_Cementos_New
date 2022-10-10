from django.contrib import admin

# Register your models here.
from .models import (
    DomainRisk,
    Risk,
    RiskMaster,
    RiskCompany
)


@admin.register(DomainRisk)
class DomainRiskAdmin(admin.ModelAdmin):
    model = DomainRisk
    list_display = ('ref', 'name', )


@admin.register(RiskMaster)
class RiskMasterAdmin(admin.ModelAdmin):
    model = RiskMaster
    list_display = ('ref', 'name', 'domain_risk')


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    model = Risk
    list_display = ('ref', 'name', 'risk_master')


@admin.register(RiskCompany)
class RiskCompanyAdmin(admin.ModelAdmin):
    model = RiskCompany
    list_display = ('risk', 'company', 'active', 'expert_assign')
