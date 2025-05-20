from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied

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

from krm.companies.forms import CompanyDomainRiskEvaluatorsForm, CompanyRiskEvaluatorsForm
from krm.risks.models import RiskCompany

#from krm.users.decorators import (
    #is_global_admin,
    #user_can_edit_company,
    #user_can_edit_domain_risk_evaluator
#)
from krm.users.decorators import is_global_admin
from django.contrib.auth.decorators import login_required


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaCompanyRiskEvaluatorUpdateView(UpdateView):
    form_class = CompanyRiskEvaluatorsForm
    model = RiskCompany
    template_name = 'companies/GaCompanyRiskEvaluatorUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': self.object.company, 'url': reverse(
                'companies:ga_company_detail', kwargs={'pk': self.object.company.pk})},
            {'title': _('Asignar evaluador')},
        ]
        context['page_title'] = _(
            'Asignar un Evaluador de Riesgo Residual (RR)')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Evaluador asignado correctamente')
        )
        return reverse_lazy(
            'companies:ga_company_detail',
            kwargs={'pk': self.object.company.pk}
        )

    def get_form(self, form_class=None):
        from krm.users.models import User
        form_class = super().get_form(form_class=None)
        form_class.fields["evaluator"].queryset = self.object.company.employees.filter(
            is_active=True)
        return form_class
