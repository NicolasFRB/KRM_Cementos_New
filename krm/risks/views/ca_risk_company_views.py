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
from django.contrib.auth.decorators import login_required

from krm.users.decorators import is_company_admin

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.risks.forms import RiskCompanyUpdateForm

from krm.risks.models import RiskCompany


@method_decorator([is_company_admin, ], name='dispatch')
class CaRiskCompanyUpdateView(UpdateView):
    form_class = RiskCompanyUpdateForm
    model = RiskCompany
    template_name = 'risks_company/CaRiskCompanyUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {
                'title': _('Dashboard'),
                'url': reverse('users:dashboard')
            },
            {'title': _('Editar')}
        ]
        context['page_title'] = _('Editar Riesgo Compañía')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Riesgo-Compañía actualizado correctamente')
        )
        return reverse_lazy(
            'companies:ca_company_detail',
            kwargs={'pk': self.object.company.pk}
        )
