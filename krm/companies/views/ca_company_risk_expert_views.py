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

from krm.companies.forms import CompanyRiskExpertsForm
from krm.risks.models import RiskCompany

#from krm.users.decorators import (
    #is_global_admin,
    #user_can_edit_company,
    #user_can_edit_domain_risk_expert
#)
from krm.users.decorators import is_company_admin
from django.contrib.auth.decorators import login_required


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class CaCompanyRiskExpertUpdateView(UpdateView):
    form_class = CompanyRiskExpertsForm
    model = RiskCompany
    template_name = 'companies/CaCompanyRiskExpertUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ca_company_list')},
            {'title': self.object.company, 'url': reverse(
                'companies:ca_company_detail', kwargs={'pk': self.object.company.pk})},
            {'title': _('Asignar Evaluador')},
        ]
        context['page_title'] = _('Asignar un Evaluador de Riesgo Inherente')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Evaluador (RI) asignado correctamente')
        )
        return reverse_lazy(
            'companies:ca_company_detail',
            kwargs={'pk': self.object.company.pk}
        )

    def get_form(self, form_class=None):
        from krm.users.models import User
        form_class = super().get_form(form_class=None)
        form_class.fields["expert"].queryset = self.object.company.employees.filter(
            is_active=True)
        return form_class
