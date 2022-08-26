# from django import forms
# from django.forms import ModelForm
# from django.utils.translation import ugettext_lazy as _

# from krc.business_group.models import Region

# from crispy_forms.helper import FormHelper
# from crispy_forms.layout import(
#     Layout, Fieldset,
#     HTML, Field)

# from django_countries.data import COUNTRIES


# class RegionCreateForm(ModelForm):
#     class Meta:
#         model = Region
#         fields = [
#             'name',
#             'description',
#             'business_group',
#             'countries',
#         ]
#         widgets = {'business_group': forms.HiddenInput()}

#     def __init__(self, *argv, **kwargs):
#         super(RegionCreateForm, self).__init__(*argv, **kwargs)
#         self.fields['countries'].widget.attrs['class'] = 'kt-select2'
#         self.fields['countries'].required = False
