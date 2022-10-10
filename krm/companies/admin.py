# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

# from tinymce.models import HTMLField

from django.forms import ModelForm
from django import forms

from krm.companies.models import (
    Company,
    CompanyDomainRiskExperts,
    CompanyDomainRiskEvaluator
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('ref', 'name', 'vat', 'address',
                    'state', 'cp', 'country', 'email')


@admin.register(CompanyDomainRiskExperts)
class CompanyDomainRiskExpertsAdmin(admin.ModelAdmin):
    model = CompanyDomainRiskExperts
    list_display = ('company', 'domain_risk', 'expert')


@admin.register(CompanyDomainRiskEvaluator)
class CompanyDomainRiskEvaluator(admin.ModelAdmin):
    model = CompanyDomainRiskEvaluator
    list_display = ('company', 'domain_risk', )
