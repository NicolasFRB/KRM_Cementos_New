# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

# from tinymce.models import HTMLField

from django.forms import ModelForm
from django import forms

from krm.companies.models import (
    Company,
)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('name', 'vat', 'address',
                    'state', 'cp', 'country', 'email')
