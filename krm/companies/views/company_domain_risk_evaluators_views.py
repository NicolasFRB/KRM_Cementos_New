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

from krm.companies.forms import CompanyDomainRiskEvaluatorsForm
from krm.companies.models import CompanyDomainRiskEvaluator

from krm.users.decorators import (
    is_global_admin,
    user_can_edit_company,
    user_can_edit_domain_risk_evaluator
)


@method_decorator([login_required, ], name='dispatch')
class GaCompanyDomainRiskEvaluatorUpdateView(UpdateView):
    form_class = CompanyDomainRiskEvaluatorsForm
    model = CompanyDomainRiskEvaluator
    template_name = 'companies/GaCompanyDomainRiskEvaluatorUpdate.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_company_admin:
            return HttpResponseRedirect(reverse('companies:ca_company_assign_evaluator_update', kwargs={'pk': kwargs['pk']}))
        if request.user.is_superuser:
            return super().dispatch(request, *args, **kwargs)
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': self.object.company, 'url': reverse(
                'companies:ga_company_detail', kwargs={'pk': self.object.company.pk})},
            {'title': _('Asignar evaluadores')},
        ]
        context['page_title'] = _(
            'Asignar Evaluadores de Riesgo Residual (RR)')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Evaluadores asignados correctamente')
        )
        return reverse_lazy(
            'companies:ga_company_detail',
            kwargs={'pk': self.object.company.pk}
        )

    def get_form(self, form_class=None):
        from krm.users.models import User
        form_class = super().get_form(form_class=None)
        form_class.fields["evaluator"].queryset = self.object.company.employees.all(
        )
        return form_class
