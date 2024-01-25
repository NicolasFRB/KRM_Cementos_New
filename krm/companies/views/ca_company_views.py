from re import template
from django.shortcuts import render
from django.db.models import Count

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms import formset_factory

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

from krm.companies.forms import CompanyCreateForm, CompanyKrmRiskSelectForm
from krm.companies.models import Company
from krm.risks.models import (
    RiskCompany,
    DomainRisk,
    RiskMaster
)

from krm.users.decorators import (
    is_global_admin,
    is_company_admin,
    user_can_edit_company
)


@method_decorator([is_company_admin, ], name='dispatch')
class CaCompanyListView(ListView):
    model = Company
    template_name = 'companies/CaCompanyList.html'
    context_object_name = 'companies'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías que administra'), 'url': reverse(
                'companies:ca_company_list')},
        ]
        context['page_title'] = _('Companías que administra')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_queryset(self):
        return self.request.user.companies_admin.all()


@method_decorator([user_can_edit_company, ], name='dispatch')
class CaCompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/CaCompanyDetail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ca_company_list')},
            {'title': self.object.vat}
        ]
        context['page_title'] = f"{_('Compañía')} : {self.object.name}"
        context['breadcrums'] = breadcrums

        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([user_can_edit_company, ], name='dispatch')
class CaCompanyUpdateView(UpdateView):
    form_class = CompanyCreateForm
    model = Company
    template_name = 'companies/CaCompanyCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ca_company_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Compañía')
        context['breadcrums'] = breadcrums

        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Compañía actualizada correctamente')
        )
        return reverse_lazy(
            'companies:ca_company_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([is_company_admin, ], name='dispatch')
class CaCompanyRiskKrmSelectView(FormView):
    form_class = CompanyKrmRiskSelectForm
    template_name = 'companies/CaCompanyRiskKrmSelect.html'

    def dispatch(self, request, *args, **kwargs):
        self.company = get_object_or_404(
            Company, pk=self.kwargs.get("pk"))
        return super(CaCompanyRiskKrmSelectView, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ca_company_list')},
            {'title': self.company.name, 'url': reverse(
                'companies:ca_company_detail', kwargs={'pk': self.company.pk})},
            {'title': _(
                'Selección de Riesgos (N2) que aplican a %s' % self.company.name)},
        ]
        context['page_title'] = _(
            'Selección de Riesgos (N2) que aplican a %s' % self.company.name)
        context['breadcrums'] = breadcrums

        context['risks_companies'] = RiskCompany.objects.filter(
            company=self.company.pk).order_by('risk__risk_master', 'risk')
        context['domain_risks'] = DomainRisk.objects.annotate(
            risks_count=Count('risks')).filter(risks_count__gt=0)
        context['risks_masters'] = RiskMaster.objects.annotate(
            risks_count=Count('risks')).filter(risks_count__gt=0)
        context['company'] = self.company

        dm = {}
        for risk_company in self.company.krm_risks.all():
            dm_pk = str(risk_company.risk.risk_master.domain_risk.pk)
            if dm_pk in dm:
                dm[dm_pk]['risks'].append(risk_company)
            else:
                dm[dm_pk] = {}
                dm[dm_pk]['name'] = risk_company.risk.risk_master.domain_risk.name
                dm[dm_pk]['risks'] = []
                dm[dm_pk]['risks'].append(risk_company)

        context['dms'] = dm
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def post(self, request, *args, **kwargs):
        risk_company_selected = request.POST.get('selectedPKs')
        risk_company_selected = risk_company_selected.split(',')
        
        self.company.krm_risks.filter(
            pk__in=risk_company_selected).update(active=True)
        self.company.krm_risks.exclude(
            pk__in=risk_company_selected).update(active=False)

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Riesgos (N2) que aplican sobre %s actualizados correctamente" % self.company.name)
        )

        return HttpResponseRedirect(
            reverse_lazy(
                'companies:ca_company_detail',
                kwargs={'pk': self.company.pk}
            )
        )
