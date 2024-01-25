from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    View
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.utils.decorators import method_decorator

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.companies.forms import CompanyDomainRiskExpertsForm
from krm.companies.models import Company, CompanyControls
from krm.companies.forms import ControlCompanyUpdateForm


from krm.users.decorators import is_global_admin


class GaCompanyControlUpdate(UpdateView):
    form_class = ControlCompanyUpdateForm
    model = CompanyControls
    template_name = 'companies/GaCompanyControlUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': self.object.company, 'url': reverse(
                'companies:ga_company_detail', kwargs={'pk': self.object.company.pk})},
            {'title': _('Asignar control owners y supervisores a un Control')},
        ]
        context['page_title'] = _(
            'Asignar control owners y supervisores a un Control')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Control-Compañía modificado correctamente')
        )
        return reverse_lazy(
            'companies:ga_company_detail',
            kwargs={'pk': self.object.company.pk}
        )

    def get_form(self, form_class=None):
        form_class = super().get_form(form_class=None)
        from krm.users.models import User

        users = User.objects.filter(
            companies=self.object.company,
            is_active=True
        )
        form_class.fields["control_test_owners"].queryset = users
        form_class.fields["control_test_supervisors"].queryset = users
        return form_class

class CaCompanyControlUpdate(UpdateView):
    form_class = ControlCompanyUpdateForm
    model = CompanyControls
    template_name = 'companies/CaCompanyControlUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ca_company_list')},
            {'title': self.object.company, 'url': reverse(
                'companies:ca_company_detail', kwargs={'pk': self.object.company.pk})},
            {'title': _('Asignar control owners y supervisores a un Control')},
        ]
        context['page_title'] = _(
            'Asignar control owners y supervisores a un Control')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Control-Compañía modificado correctamente')
        )
        return reverse_lazy(
            'companies:ca_company_detail',
            kwargs={'pk': self.object.company.pk}
        )

    def get_form(self, form_class=None):
        form_class = super().get_form(form_class=None)
        from krm.users.models import User

        users = User.objects.filter(
            companies=self.object.company,
            is_active=True
        )
        form_class.fields["control_test_owners"].queryset = users
        form_class.fields["control_test_supervisors"].queryset = users
        return form_class
