import re
from openpyxl import load_workbook
from io import BytesIO
import re


from django.views.generic import (
    FormView,
    DetailView,
    UpdateView,
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.configuration.forms import ConfigurationUpdateForm, ImportForm
from krm.configuration.models import Configuration

from krm.companies.models import Company

from krm.risks.models import (
    Risk,
    RiskMaster,
    DomainRisk,
    RiskCompany
)

from krm.controls.models import (
    Control
)

from krm.process.models import (
    SubProcess,
)


@method_decorator([login_required, ], name='dispatch')
class ConfigurationDetailView(DetailView):
    model = Configuration
    template_name = 'configuration/ConfigurationDetail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Configuración'), 'url': reverse(
                'configuration:configuration_detail')},
        ]
        context['page_title'] = _('Configuración Global')
        context['breadcrums'] = breadcrums
        return context

    def get_object(self):
        return Configuration.objects.first()


@method_decorator([login_required, ], name='dispatch')
class ConfigurationUpdateView(UpdateView):
    form_class = ConfigurationUpdateForm
    model = Configuration
    template_name = 'configuration/ConfigurationUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Configuración'), 'url': reverse(
                'configuration:configuration_detail')},
            {'title': _('Editar'), 'url': reverse(
                'configuration:configuration_update')},
        ]
        context['page_title'] = _('Editar Configuración Global')
        context['breadcrums'] = breadcrums
        return context

    def get_object(self):
        return Configuration.objects.first()

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Configuración actualizada correctamente')
        )
        return reverse_lazy(
            'configuration:configuration_detail'
        )


@method_decorator([login_required, ], name='dispatch')
class GaImportView(FormView):
    template_name = 'configuration/GaImport.html'
    form_class = ImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Importador')},
        ]
        context['page_title'] = _('Importador')
        context['breadcrums'] = breadcrums
        return context

    def form_valid(self, form):
        input_excel = self.request.FILES['data_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)

        # Dominios de Riesgo
        domain_risk_sheet = wb['Domain Risk']
        domain_risk_to_create = []
        nrow = 0
        rows = domain_risk_sheet.rows
        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            domain_risk = {}
            if row[0].value is None:
                break
            # Los dominios de riesgo hay que validarlos y ver que existen y que no hay nada raro
            domain_risk['ref'] = row[0].value.strip().upper()
            domain_risk['name'] = row[1].value
            domain_risk['description'] = row[2].value
            for r in domain_risk_to_create:
                if r['ref'] == domain_risk['ref']:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de dominios de riesgo hay una REF repetida: %s en la fila %s')
                            % (r['ref'], nrow)
                        ),
                    )
                    return super(GaImportView, self).form_invalid(form)
            domain_risk_to_create.append(domain_risk)

        # Validate domain_risk_to_create
        for dr in domain_risk_to_create:
            if DomainRisk.objects.filter(ref=dr['ref']).count() > 0:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de dominios de riesgo hay una REF que ya existe: %s')
                        % (dr['ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

        # Riesgos Maestros
        risk_master_sheet = wb['Risk Master N1']
        risk_master_to_create = []
        nrow = 0
        rows = risk_master_sheet.rows
        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            risk_master = {}
            # Los dominios de riesgo hay que validarlos y ver que existen y que no hay nada raro
            if row[0].value is None:
                break
            risk_master['domain_risk_ref'] = row[0].value.strip().replace(
                ' ', '').upper()
            risk_master['ref'] = row[1].value.strip().replace(' ', '').upper()
            risk_master['name'] = row[2].value
            risk_master['description'] = row[3].value

            for rm in risk_master_to_create:
                if rm['ref'] == risk_master['ref']:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de riesgos maestros hay una REF repetida: %s')
                            % (rm['ref'])
                        ),
                    )
                    return super(GaImportView, self).form_invalid(form)

            risk_master_to_create.append(risk_master)

        for rm in risk_master_to_create:
            if RiskMaster.objects.filter(ref=rm['ref']).count() > 0:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de riesgos maestros hay una REF que ya existe: %s')
                        % (rm['ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            domain_risk_exist = False
            if DomainRisk.objects.filter(ref=rm['domain_risk_ref']).count() > 0:
                domain_risk_exist = True

            # Si no existe buscamos si está en la hora de dominios de riesgo a crear
            for dr in domain_risk_to_create:
                if rm['domain_risk_ref'] == dr['ref']:
                    domain_risk_exist = True

            if not domain_risk_exist:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de riesgo maestro hay una REF de dominio de riesgo que no existe: %s')
                        % (rm['domain_risk_ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

        # Riesgos
        risk_sheet = wb['Risk N2']
        risk_to_create = []
        nrow = 0
        rows = risk_sheet.rows

        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            risk = {}

            if row[0].value is None:
                break
            risk['risk_master_ref'] = row[0].value.strip().replace(' ',
                                                                   '').upper()
            risk['ref'] = row[1].value.strip().replace(' ', '').upper()
            risk['name'] = row[2].value
            risk['description'] = row[3].value
            risk['impact_inherent'] = row[4].value
            risk['impact_residual'] = row[5].value
            risk['probability_inherent'] = row[6].value
            risk['probability_residual'] = row[7].value
            risk['krm_activity_affected'] = row[8].value
            risk['krm_main_events'] = row[9].value
            risk['krm_exposed_staff'] = row[10].value
            risk['krm_main_elements'] = row[11].value
            if risk['impact_inherent'] not in range(1, 6) or risk['impact_residual'] not in range(1, 6) or risk['probability_inherent'] not in range(1, 6) or risk['probability_residual'] not in range(1, 6):
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('Impacto o probabilidad erróneos en la fila: %s')
                        % (nrow)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            for r in risk_to_create:
                if r['ref'] == risk['ref']:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de riesgos hay una REF repetida: %s en la fila %s')
                            % (r['ref'], nrow)
                        ),
                    )
                    return super(GaImportView, self).form_invalid(form)

            risk_to_create.append(risk)

        for r in risk_to_create:
            if Risk.objects.filter(ref=r['ref']).count() > 0:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de riesgos hay una REF que ya existe: %s')
                        % (r['ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            risk_master_exist = False
            if RiskMaster.objects.filter(ref=r['risk_master_ref']).count() > 0:
                risk_master_exist = True

            # Si no existe buscamos si está en la hora de dominios de riesgo a crear
            for rm in risk_master_to_create:
                if r['risk_master_ref'] == rm['ref']:
                    risk_master_exist = True

            if not risk_master_exist:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de riesgos hay una REF de riesgo maestro que no existe: %s')
                        % (r['risk_master_ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

        # Controles
        control_sheet = wb['Controls']
        control_to_create = []
        nrow = 0
        rows = control_sheet.rows

        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            control = {}

            if row[0].value is None:
                break
            if row[0].value is not None:
                control['risk_refs'] = row[0].value.replace(
                    ' ', '').upper().split(',')
            else:
                control['risk_refs'] = []

            if row[1].value is not None:
                control['sub_process_refs'] = row[1].value.replace(
                    ' ', '').upper().split(',')
            else:
                control['sub_process_refs'] = []

            control['ref'] = row[2].value.strip().upper()
            control['name'] = row[3].value
            control['description'] = row[4].value
            control['testing_procedure'] = row[5].value
            control['key_control'] = row[6].value
            control['control_type'] = row[7].value
            control['automation'] = row[8].value
            control['systems'] = row[9].value
            control['control_frequency'] = row[10].value
            control['is_gap'] = row[11].value
            control['assert_existence'] = row[12].value
            control['assert_completeness'] = row[13].value
            control['assert_valuation'] = row[14].value
            control['assert_rights'] = row[15].value
            control['assert_disclosure'] = row[16].value
            control['assert_accurancy'] = row[17].value
            control['assert_froud'] = row[18].value

            if control['automation'] == '':
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de controles no ha establecido valor para Control Automation en la fila %s')
                        % (nrow+1)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            if control['control_frequency'] not in ('BD', 'DI', '1W', '2W', '1M', '3T', '6M', '1Y'):
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de controles no ha establecido valor para Control Frequency en la fila %s')
                        % (nrow+1)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            if control['is_gap'] not in ('Y', 'N', '-') or control['assert_existence'] not in ('Y', 'N', '-') or control['assert_completeness'] not in ('Y', 'N', '-') or control['assert_valuation'] not in ('Y', 'N', '-') or control['assert_rights'] not in ('Y', 'N', '-') or control['assert_disclosure'] not in ('Y', 'N', '-') or control['assert_accurancy'] not in ('Y', 'N', '-') or control['assert_froud'] not in ('Y', 'N', '-'):
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de controles no ha establecido valor para alguna celda obligatoria en la fila %s')
                        % (nrow+1)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            for c in control_to_create:
                if c['ref'] == control['ref']:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de controles hay una REF repetida: %s en la fila %s')
                            % (c['ref'], nrow+1)
                        ),
                    )
                    return super(GaImportView, self).form_invalid(form)

            nrow += 1
            control_to_create.append(control)

        for c in control_to_create:
            if Control.objects.filter(ref=c['ref']).count() > 0:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de controles hay una REF de control que ya existe: %s')
                        % (c['ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            for risk_ref in c['risk_refs']:
                risk_exist = False
                if Risk.objects.filter(ref=risk_ref).count() > 0:
                    risk_exist = True
                else:
                    for risk in risk_to_create:
                        if risk_ref == risk['ref']:
                            risk_exist = True
                if not risk_exist:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de controles hay una REF a un riesgo que no existe: %s')
                            % (risk_ref)
                        ),
                    )
                    return super(GaImportView, self).form_invalid(form)

            for subprocess_ref in c['sub_process_refs']:

                if SubProcess.objects.filter(ref=subprocess_ref).count() == 0:
                    print(subprocess_ref)
                    import ipdb
                    ipdb.set_trace()
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de controles hay una REF a un subproceso que no existe: %s')
                            % (subprocess_ref)
                        ),
                    )
                    return super(GaImportView, self).form_invalid(form)

        # Riesgos Compañías
        risk_sheet = wb['RiskCompany']
        risk_company_to_create = []
        nrow = 0
        rows = risk_sheet.rows

        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            risk_company = {}

            if row[0].value is None:
                break
            risk_company['risk_ref'] = row[0].value.strip().replace(
                ' ', '').upper()
            risk_company['company_ref'] = row[1].value.strip().replace(
                ' ', '').upper()

            risk_company_to_create.append(risk_company)

        for r in risk_company_to_create:
            if Risk.objects.filter(ref=r['risk_ref']).count() == 0:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de riesgo compañía hay una REF de riesgo que no existe: %s')
                        % (r['risk_ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            if Company.objects.filter(ref=r['company_ref']).count() == 0:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de riesgo compañía hay una REF a una compañía que no existe: %s')
                        % (r['company_ref'])
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

        # Vamos a crear cosas
        dr_created = 0
        for dr in domain_risk_to_create:
            DomainRisk.objects.create(
                ref=dr['ref'],
                name=dr['name'],
                description=dr['description']
            )
            dr_created += 1

        if dr_created > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                (
                    _(
                        "{0} Dominios de Riesgo importados"
                    ).format(
                        dr_created,
                    )
                ),
            )

        rm_created = 0
        for rm in risk_master_to_create:
            RiskMaster.objects.create(
                ref=rm['ref'],
                name=rm['name'],
                description=rm['description'],
                domain_risk=DomainRisk.objects.get(ref=rm['domain_risk_ref'])
            )
            rm_created += 1

        if rm_created > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                (
                    _(
                        "{0} Riesgos Maestros importados"
                    ).format(
                        rm_created,
                    )
                ),
            )

        r_created = 0
        for r in risk_to_create:
            Risk.objects.create(
                ref=r['ref'],
                name=r['name'],
                description=r['description'],
                risk_master=RiskMaster.objects.get(ref=r['risk_master_ref']),
                impact_inherent=r['impact_inherent'],
                probability_inherent=r['probability_inherent'],
                impact_residual=r['impact_residual'],
                probability_residual=r['probability_residual'],
                krm_activity_affected=r['krm_activity_affected'],
                krm_main_events=r['krm_main_events'],
                krm_exposed_staff=r['krm_exposed_staff'],
                krm_main_elements=r['krm_main_elements'],
            )
            r_created += 1

        c_created = 0
        for r in control_to_create:
            key_control = False
            if r['key_control'] == 'X':
                key_control = True
            new_control = Control.objects.create(
                ref=r['ref'],
                name=r['name'],
                description=r['description'],
                testing_procedure=r['testing_procedure'],
                key_control=key_control,
                control_type=r['control_type'],
                automation=r['automation'],
                systems=r['systems'],
                control_frequency=r['control_frequency'],
                is_gap=r['is_gap'],
                assert_existence=r['assert_existence'],
                assert_completeness=r['assert_completeness'],
                assert_valuation=r['assert_valuation'],
                assert_rights=r['assert_rights'],
                assert_disclosure=r['assert_disclosure'],
                assert_accurancy=r['assert_accurancy'],
                assert_froud=r['assert_froud'],
            )

            if Risk.objects.filter(
                    ref__in=r['risk_refs']).count() > 0:
                for risk_to_add in Risk.objects.filter(
                        ref__in=r['risk_refs']):
                    new_control.risks.add(risk_to_add)
            if SubProcess.objects.filter(
                    ref__in=r['sub_process_refs']).count() > 0:
                for sub_process_to_add in SubProcess.objects.filter(
                        ref__in=r['sub_process_refs']):
                    new_control.sub_processes.add(sub_process_to_add)
            c_created += 1

        if c_created > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                (
                    _(
                        "{0} Controles importados"
                    ).format(
                        c_created,
                    )
                ),
            )

        # RiskCompany
        risk_company_created = 0
        for rc in risk_company_to_create:
            rc_object = RiskCompany.objects.get(
                company__ref=rc['company_ref'],
                risk__ref=rc['risk_ref']
            )
            rc_object.active = True
            rc_object.save()
            risk_company_created += 1

        if risk_company_created > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                (
                    _(
                        "{0} Riesgos Compañía creados"
                    ).format(
                        risk_company_created,
                    )
                ),
            )

        return super(GaImportView, self).form_valid(form)

    def get_success_url(self):

        return reverse_lazy("configuration:ga_import")
