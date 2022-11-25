from django.db.models import Count
from openpyxl import load_workbook
from io import BytesIO

import re

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

from krm.companies.forms import (
    CompanyCreateForm,
    CompanyKrmRiskSelectForm,
    CompanyImportForm
)

from krm.companies.models import Company
from krm.risks.models import (
    RiskCompany,
    DomainRisk,
    RiskMaster
)

from krm.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyListView(ListView):
    model = Company
    template_name = 'companies/GaCompanyList.html'
    context_object_name = 'companies'
    queryset = Company.objects.all()
    # .prefetch_related('krm_risks').all()\
    # .annotate(n_risks=Count('krm_risks', distinct=True))
    # .prefetch_related('companydomainriskevaluator').all()\
    # .prefetch_related('krm_risks_active').all()\

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
        ]
        context['page_title'] = _('Companías')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('companies:ga_company_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyDetailView(DetailView):
    model = Company
    template_name = 'companies/GaCompanyDetail.html'
    context_object_name = 'company'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': self.object.vat}
        ]
        context['page_title'] = f"{_('Compañía')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('companies:ga_company_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyCreateView(CreateView):
    form_class = CompanyCreateForm
    model = Company
    template_name = 'companies/GaCompanyCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': _('Nueva Compañía'), 'url': reverse(
                'companies:ga_company_create')},
        ]
        context['page_title'] = _('Nueva Compañía')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Compañía creada correctamente')
        )

        return reverse_lazy(
            'companies:ga_company_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyUpdateView(UpdateView):
    form_class = CompanyCreateForm
    model = Company
    template_name = 'companies/GaCompanyCreate.html'

    def get_form(self, *args, **kwargs):
        form = super(GaCompanyUpdateView, self).get_form(*args, **kwargs)
        if self.object:
            form.fields['evaluators'].queryset = self.object.employees.all()
        return form

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
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
            'companies:ga_company_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyDeleteView(DeleteView):
    model = Company
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Compañía")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Compañía eliminada correctamente")
        )
        return reverse_lazy("companies:ga_company_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar la Companía y todas sus evaluaciónes?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados la misma.</span>'
        ).format(str(self.object))


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyRiskKrmSelectView(FormView):
    form_class = CompanyKrmRiskSelectForm
    template_name = 'companies/GaCompanyRiskKrmSelect.html'

    def dispatch(self, request, *args, **kwargs):
        self.company = get_object_or_404(
            Company, pk=self.kwargs.get("pk"))
        return super(GaCompanyRiskKrmSelectView, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': self.company.name, 'url': reverse(
                'companies:ga_company_detail', kwargs={'pk': self.company.pk})},
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
        risk_company_selected = request.POST.getlist('risk_pk')
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
                'companies:ga_company_detail',
                kwargs={'pk': self.company.pk}
            )
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaCompanyImportView(FormView):
    template_name = 'companies/GaCompanyImport.html'
    form_class = CompanyImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Compañías'), 'url': reverse(
                'companies:ga_company_list')},
            {'title': _('Importar Compañías')},
        ]
        context['page_title'] = _('Importar Companías')
        context['breadcrums'] = breadcrums
        return context

    def form_valid(self, form):
        companies_to_create = []

        input_excel = self.request.FILES['companies_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)
        sheet = wb.active

        nrow = 0
        rows = sheet.rows
        for row in rows:
            if nrow < 2:
                nrow += 1
                continue

            company = {}
            # Comprobamos que hay contenido en todas las celdas obligatorias
            if row[0].value is None:
                break

            if row[0].value is not None or row[1].value is not None:
                company['ref'] = str(row[0].value).title()
                company['name'] = str(row[1].value).title()
                company['vat'] = str(row[2].value).title()
                company['address'] = str(row[3].value)
                company['state'] = str(row[4].value).upper()
                cell = row[5]
                cell_value = cell.value
                try:
                    cell_value = int(cell_value)
                except:
                    cell_value = None
                company['cp'] = cell_value
                if row[7].value is not None:
                    company['country'] = str(row[6].value).upper()
                else:
                    company['country'] = None
                company['email'] = str(
                    row[8].value).lower().replace(' ', '')
                company['type_company'] = str(row[9].value)
                company['companies_in_scope'] = str(row[10].value)

                # Tenemos que comprobar que el email esté bien formado
                if company['email'] != '':
                    if not re.match(
                        '^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',
                        company['email'].lower()
                    ):
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la fila %s el email introducido no es correcto. Se ha abortado la importación') % str(
                                    nrow+1)
                            )
                        )
                        return super(
                            GaCompanyImportView,
                            self
                        ).form_invalid(form)
                        break

                if Company.objects.filter(ref=company['ref']).count() > 0:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('La REF introducida en la fila %s ya está registrado por otra compañía') % str(
                                nrow+1)
                        )
                    )
                    return super(
                        GaCompanyImportView,
                        self
                    ).form_invalid(form)
                    break

                if Company.objects.filter(vat=company['vat']).count() > 0:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('El VAT introducido en la fila %s ya está registrado por otra compañía') % str(
                                nrow+1)
                        )
                    )
                    return super(
                        GaCompanyImportView,
                        self
                    ).form_invalid(form)
                    break

            else:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la fila %s falta algún campo obligatorio. Se ha abortado la importación') % str(
                            nrow+1)
                    )
                )
                return super(
                    GaCompanyImportView,
                    self
                ).form_invalid(form)
                break

            nrow += 1

            companies_to_create.append(company)

        for c in companies_to_create:
            Company.objects.create(
                ref=c['ref'],
                name=c['name'],
                vat=c['vat'],
                address=c['address'],
                cp=c['cp'],
                email=c['email'],
                state=c['state'],
                country=c['country'],
                type_company=c['type_company'],
                companies_in_scope=c['companies_in_scope'],
            )

        messages.add_message(
            self.request,
            messages.SUCCESS, (
                _('Se han importado %s compañías') % str(len(companies_to_create)))
        )

        return super(GaCompanyImportView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('companies:ga_company_list')
