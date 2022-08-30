from django.contrib import admin

# Register your models here.
from .models import DomainRisk, Risk


@admin.register(DomainRisk)
class DomainRiskAdmin(admin.ModelAdmin):
    model = DomainRisk
    list_display = ('ref', 'name', )


@admin.register(Risk)
class RiskAdmin(admin.ModelAdmin):
    model = Risk
    list_display = ('ref', 'name', 'domain_risk')
