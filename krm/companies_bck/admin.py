# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.utils.safestring import mark_safe

from tinymce.models import HTMLField

from django.forms import ModelForm
from django import forms

from krc.business_group.models import (
    BusinessGroup,
    Company
)


# class BookingLineInline(admin.StackedInline):
#     model = BookingLine
#     fields = ['booking', 'n_participants', 'display_text', 'price', 'subtract_quota']
#     readonly_fields = ('booking', 'created', 'modified')

# @admin.register(Booking)
# class BookingAdmin(ImportExportModelAdmin):
#     model = Booking
#     list_display = ('code', 'date', 'visit', 'origin',
#                     'external_reference', 'status',
#                     'lang', 'guide', 'name', 'email',
#                     'n_participants', 'n_participants_total', 'total',
#                     'created',)
#     readonly_fields = ( 'code', 'private_description', 'n_participants',
#                         'n_participants_total', 'total', 'order_tpv',
#                         'tpv_error', 'tpv_error_info', 'payment_method',
#                         'created', 'modified')
#     inlines = [BookingLineInline]
#     list_filter = ( ('date', DateRangeFilter),
#                     ('origin', admin.RelatedOnlyFieldListFilter),
#                     ('visit', admin.RelatedOnlyFieldListFilter),
#                     ('guide', admin.RelatedOnlyFieldListFilter),
#                     'status',
#                     'incidence',
#                     ('created', DateRangeFilter)
#                     )
#     resource_class = BookingResource
from django_countries.widgets import CountrySelectWidget
from django_countries.data import COUNTRIES


class CompanyInline(admin.TabularInline):
    model = Company
    classes = ['collapse']


@admin.register(BusinessGroup)
class BusinessGroupAdmin(admin.ModelAdmin):
    model = BusinessGroup
    list_display = ('name', 'vat', 'address', 'state', 'cp', 'country', 'email')


# @admin.register(Region)
# class RegionAdmin(admin.ModelAdmin):
#     model = Region
#     form = RegionForm
#     list_display = ('name', 'business_group', 'description', 'countries_list')
#     inlines = [
#         CompanyInline
#     ]
#     def countries_list(self, obj):
#         return mark_safe("<br />".join([l.name for l in obj.countries]))


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    model = Company
    list_display = ('name', 'vat', 'address', 'state', 'cp', 'country', 'email')
