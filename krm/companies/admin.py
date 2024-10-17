# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

# from tinymce.models import HTMLField

from django.forms import ModelForm
from django import forms

from krm.companies.models import (
    Company,
    CompanyDomainRiskExperts,
    CompanyDomainRiskEvaluator,
    CompanyControls,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('ref', 'name', 'vat', 'address',
                    'state', 'cp', 'country', 'email')
    # filter_horizontal = (
    #     'controls',
    # )


@admin.register(CompanyDomainRiskExperts)
class CompanyDomainRiskExpertsAdmin(admin.ModelAdmin):
    model = CompanyDomainRiskExperts
    list_display = ('company', 'domain_risk', 'expert')


@admin.register(CompanyDomainRiskEvaluator)
class CompanyDomainRiskEvaluator(admin.ModelAdmin):
    model = CompanyDomainRiskEvaluator
    list_display = ('company', 'domain_risk', )


@admin.register(CompanyControls)
class CompanyControls(admin.ModelAdmin):
    model = CompanyControls
    list_display = ('pk', 'company', 'active', 'control')
    filter_horizontal = (
        'control_test_owners',
        'control_test_supervisors'
    )
    list_filter = ('active', 'company', 'control__block')
