from django.db.models import Count
from openpyxl import load_workbook
from io import BytesIO

import re

#import login_required
from django.contrib.auth.decorators import login_required

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


@method_decorator([login_required, is_global_admin, ], name='dispatch')
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
        context['page_title'] = _('Compañías')
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


@method_decorator([login_required, is_global_admin, ], name='dispatch')
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


@method_decorator([login_required, is_global_admin, ], name='dispatch')
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


@method_decorator([login_required, is_global_admin, ], name='dispatch')
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


@method_decorator([login_required, is_global_admin, ], name='dispatch')
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


@method_decorator([login_required, is_global_admin, ], name='dispatch')
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
                'companies:ga_company_detail',
                kwargs={'pk': self.company.pk}
            )
        )

@method_decorator([login_required, is_global_admin, ], name='dispatch')
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

    def checkDB(self, name, elem, DBreference, field_key, index):
        """
        Función que contrasta si existen previamente en la base de datos instancias de un objeto con el mismo identificador (ref) o atributo único (vat)
        que alguna de las nuevas instancias que se pretende crear.

        Parameters
        -----------
        name: String.
            Nombre del objeto del cual se quiere crear una instancia con una referencia repetida.
        elem: dict.
            Diccionario de python que contiene los valores de los atributos de la nueva instancia del objeto que queremos crear y para el cual
            estamos realizando esta validación.
        DBreference: Referencia a objeto.
            Es la clase de Python que nos define el tipo de objeto que se está intentando crear.
        form: form.
            Formulario ya validado asociado a la vista.
        field_key: String.
            Nombre del atributo cuya repetición se quiere contrastar.

        """
        problem= False
        if field_key == "ref":
            if DBreference.objects.filter(ref=elem[field_key]).count() > 0:
                self.errors_found +=1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('El campo %s del usuario de la fila %s (%s) ya se encuentra registrado, por favor aporte un nuevo valor')
                        % (name, index, elem[field_key])
                    ),
                )
                problem= True
        else:
            if DBreference.objects.filter(vat=elem[field_key]).count() > 0:
                self.errors_found +=1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('El campo %(name)s del usuario de la fila %(index)s (%(value)s) ya se encuentra registrado, por favor aporte un nuevo valor') % {
                            "name": name,
                            "index": index,
                            "value": elem[field_key]
                        }
                    ),
                )
                problem= True
        return problem

    def checkExcelRep(self, name, elem, elems_to_create, index, field_key):
        """
        Función empleada para contrastar que no existe una instancia de un objeto con el mismo valor para
        el atributo field_key en la importación de datos, que en este caso será la referencia o el VAT, dado
        que este funciona como identificador de la instancia (NMB). Es decir, se contrasta que no existen dos instancias en
        una pestaña de importación que contengan el mismo valor para dichos atributos únicos.

        Parameters
        ----------
        name: String.
            Nombre del objeto del cual se quiere crear una instancia con una referencia repetida.
        elem: dict.
            Diccionario de python que contiene los valores de los atributos de la nueva instancia del objeto que queremos crear y para el cual
            estamos realizando esta validación.
        elems_to_create: list.
            Lista que contiene diccionarios con los datos de las nuevas instancias a crear de la pestaña name.
        form: form.
            Formulario ya validado asociado a la vista.
        index: int.
            Número entero que nos indica la fila en la que se encuentra el error de referencia repetida que será la de número index+1.
        field_key: String.
            Nombre del atributo cuya repetición se quiere contrastar.

        """
        problem= False
        for e in elems_to_create:
            if e[field_key] == elem[field_key]:
                self.errors_found +=1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('El campo %s se encuentra repetido en el importador: %s en la fila %d')
                        % (name, e[field_key], index)
                    ),
                )
                problem= True
        return problem

    def form_valid(self, form):
        companies_to_create = []
        self.errors_found= 0

        input_excel = self.request.FILES['companies_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)
        rows = [row for row in wb['Companies'].iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]
        pais_codigos = [
        'AF', 'AL', 'DZ', 'AS', 'AD', 'AO', 'AI', 'AQ', 'AG', 'AR', 'AM', 'AW', 'AU', 'AT', 'AZ',
        'BS', 'BH', 'BD', 'BB', 'BY', 'BE', 'BZ', 'BJ', 'BM', 'BT', 'BO', 'BQ', 'BA', 'BW', 'BV', 'BR',
        'IO', 'BN', 'BG', 'BF', 'BI', 'CI', 'CV', 'KH', 'CM', 'CA', 'KY', 'CF', 'TD', 'CL', 'CN', 'CX',
        'CC', 'CO', 'KM', 'CG', 'CD', 'CK', 'CR', 'HR', 'CU', 'CW', 'CY', 'CZ', 'DK', 'DJ', 'DM', 'DO',
        'EC', 'EG', 'SV', 'GQ', 'ER', 'EE', 'SZ', 'ET', 'FK', 'FO', 'FJ', 'FI', 'FR', 'GF', 'PF', 'TF',
        'GA', 'GM', 'GE', 'DE', 'GH', 'GI', 'GR', 'GL', 'GD', 'GP', 'GU', 'GT', 'GG', 'GN', 'GW', 'GY',
        'HT', 'HM', 'VA', 'HN', 'HK', 'HU', 'IS', 'IN', 'ID', 'IR', 'IQ', 'IE', 'IM', 'IL', 'IT', 'JM',
        'JP', 'JE', 'JO', 'KZ', 'KE', 'KI', 'KP', 'KR', 'KW', 'KG', 'LA', 'LV', 'LB', 'LS', 'LR', 'LY',
        'LI', 'LT', 'LU', 'MO', 'MG', 'MW', 'MY', 'MV', 'ML', 'MT', 'MH', 'MQ', 'MR', 'MU', 'YT', 'MX',
        'FM', 'MD', 'MC', 'MN', 'ME', 'MS', 'MA', 'MZ', 'MM', 'NA', 'NR', 'NP', 'NL', 'NC', 'NZ', 'NI',
        'NE', 'NG', 'NU', 'NF', 'MK', 'MP', 'NO', 'OM', 'PK', 'PW', 'PS', 'PA', 'PG', 'PY', 'PE', 'PH',
        'PN', 'PL', 'PT', 'PR', 'QA', 'RE', 'RO', 'RU', 'RW', 'BL', 'SH', 'KN', 'LC', 'MF', 'PM', 'VC',
        'WS', 'SM', 'ST', 'SA', 'SN', 'RS', 'SC', 'SL', 'SG', 'SX', 'SK', 'SI', 'SB', 'SO', 'ZA', 'GS',
        'SS', 'ES', 'LK', 'SD', 'SR', 'SJ', 'SE', 'CH', 'SY', 'TW', 'TJ', 'TZ', 'TH', 'TL', 'TG', 'TK',
        'TO', 'TT', 'TN', 'TR', 'TM', 'TC', 'TV', 'UG', 'UA', 'AE', 'GB', 'UM', 'US', 'UY', 'UZ', 'VU',
        'VE', 'VN', 'VG', 'VI', 'WF', 'EH', 'YE', 'ZM', 'ZW'
        ]

        for row in rows:
            i= row[0].row
            if not i == 1:
                company = {}

                #comprobación de obligatoriedad de campos
                mandatory= row[0].value and str(row[0].value).strip()!= '' and row[1].value and str(row[1].value).strip()!= ''
                if mandatory:
                    company['ref'] = str(row[0].value)
                    company['name'] = str(row[1].value)
                    company['vat'] = str(row[2].value)
                    company['address'] = str(row[3].value)
                    company['state'] = str(row[4].value)
                    cell_value = row[5].value
                    try:
                        cell_value = int(cell_value)
                    except:
                        cell_value = None
                    company['cp'] = cell_value
                    if row[6].value is not None:
                        company['country'] = str(row[6].value)
                    else:
                        company['country'] = None
                    company['email'] = str(row[7].value).lower().strip() if row[7].value else None
                    company['type_company'] = str(row[8].value)
                    company['companies_in_scope'] = str(row[9].value)

                    #comprobaciones correspondientes a la referencia de la compañía
                    if self.checkDB("Referencia", company, Company, "ref", i):
                        return super(GaCompanyImportView, self).form_invalid(form)
                    if self.checkExcelRep("Referencia", company, companies_to_create, i, "ref"):
                        return super(GaCompanyImportView, self).form_invalid(form)

                    #comprobaciones correspondientes a la unicidad del VAT de la compañía
                    if self.checkDB("VAT", company, Company, "ref", i):
                        return super(GaCompanyImportView, self).form_invalid(form)
                    if self.checkExcelRep("VAT", company, companies_to_create, i, "vat"):
                        return super(GaCompanyImportView, self).form_invalid(form)

                    #comprobaciones con respecto a la dirección de email del usuario
                    if company['email']:
                        if not re.match(
                            '^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',
                            company['email']
                        ):
                            self.errors_found +=1
                            messages.add_message(self.request, messages.ERROR, (_('La dirección de correo introducida en la fila %s no cumple con el formato válido') % str(i)))
                            return super(GaCompanyImportView, self).form_invalid(form)

                    #comprobación correspondiente al país de la compañía
                    if company['country'] not in pais_codigos:
                        self.errors_found +=1
                        messages.add_message(self.request, messages.ERROR, (_('En la fila %s el código de país introducido no tiene formato correcto, por favor aporte uno nuevo') % str(i)))
                        return super(GaCompanyImportView, self).form_invalid(form)

                else:
                    self.errors_found +=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        ( _(u'Uno de los campos obligatorios (*) se ha dejado sin completar en la fila %s') % str(i))
                    )
                    return super(GaCompanyImportView, self).form_invalid(form)

                companies_to_create.append(company)

        if self.errors_found == 0:

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
