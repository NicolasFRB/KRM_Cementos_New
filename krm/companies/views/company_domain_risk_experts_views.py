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
from krm.companies.models import CompanyDomainRiskExperts

from krm.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyDomainRiskExpertsUpdateView(UpdateView):
    form_class = CompanyDomainRiskExpertsForm
    model = CompanyDomainRiskExperts
    template_name = 'companies/GaCompanyDomainRiskExpertsUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': self.object.company, 'url': reverse(
                'companies:ga_company_detail', kwargs={'pk': self.object.company.pk})},
            {'title': _('Asignar experto')},
        ]
        context['page_title'] = _('Asignar Experto de Riesgo Inherente (RI)')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Experto asignado correctamente')
        )
        return reverse_lazy(
            'companies:ga_company_detail',
            kwargs={'pk': self.object.company.pk}
        )

    def get_form(self, form_class=None):
        from krm.users.models import User
        form_class = super().get_form(form_class=None)
        form_class.fields["expert"].queryset = self.object.company.employees.all()
        return form_class
