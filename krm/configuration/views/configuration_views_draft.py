from openpyxl import load_workbook
from io import BytesIO
import re, datetime


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
from krm.users.models import User

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

from krm.evaluations_krm.models import (
    EvaluationKrmInherent, RiskTestInherent
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

    def checkExcelRep(name, elem, elems_to_create, self, form, index):
        for e in elems_to_create:
            if e['ref'] == elem['ref']:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de %s hay una REF repetida: %s en la fila %s')
                        % (name, e['ref'], index)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

    def checkDB(name, elem, DBreference, self, form):
        if DBreference.objects.filter(ref=elem['ref']).count() > 0:
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('En la hoja de dominios de riesgo hay una REF que ya existe: %s')
                    % (elem['ref'])
                ),
            )
            return super(GaImportView, self).form_invalid(form)

    def checkMaster(name, master_name, elem, elems_to_create, master_DBreference, master, self, form):
        exist = False
        if master_DBreference.objects.filter(ref=elem[master]).count() > 0:
            exist = True
        else: 
        # Si no existe buscamos si está en la hora de dominios de riesgo a crear
            for dr in elems_to_create:
                if elem[master] == dr['ref']:
                    exist = True

        if not exist:
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('En la hoja de %s hay una REF de %s que no existe: %s')
                    % (name, master_name, elem[master])
                ),
            )
            return super(GaImportView, self).form_invalid(form)

    def success(name, created, self):
        if created > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                (
                    _(
                        "{0} %s importados"
                    ).format(
                        created,
                    )
                ),
            )

    def form_valid(self, form):
        input_excel = self.request.FILES['data_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)
        
        # Dominios de Riesgo
        domain_risk_sheet = wb['Domain Risk']
        domain_risk_to_create = []
        rows = domain_risk_sheet.rows

        for i, row in enumerate(rows):
            domain_risk = {}
            if row[0].value is None:
                break # necesita mostrar el error

            domain_risk['ref'] = row[0].value.strip().upper()
            domain_risk['name'] = row[1].value
            domain_risk['description'] = row[2].value

            self.checkExcelRep("dominios de riesgo", domain_risk, domain_risk_to_create, self, form, i)
            self.checkDB("dominios de riesgo", domain_risk, DomainRisk, self, form)
            
            domain_risk_to_create.append(domain_risk)
        
        # Riesgos Maestros
        risk_master_sheet = wb['Risk Master N1']
        risk_master_to_create = []
        rows = risk_master_sheet.rows
        
        for i, row in enumerate(rows):
            risk_master = {}
            
            if row[0].value is None:
                break # mostrar el error
            
            risk_master['domain_risk_ref'] = row[0].value.strip().replace(' ', '').upper()
            risk_master['ref'] = row[1].value.strip().replace(' ', '').upper()
            risk_master['name'] = row[2].value
            risk_master['description'] = row[3].value

            self.checkExcelRep("riesgos maestros", risk_master, risk_master_to_create, self, form, i)
            self.checkDB("riesgos maestros", risk_master, RiskMaster, self, form)
            self.checkMaster("riesgos maestros", "dominios de riesgo", risk_master, domain_risk_to_create, DomainRisk, "domain_risk_ref", self, form)
            
            risk_master_to_create.append(risk_master)

        # Riesgos
        risk_sheet = wb['Risk N2']
        risk_to_create = []
        rows = risk_sheet.rows

        for i, row in enumerate(rows):
            risk = {}

            if row[0].value is None:
                break # mensaje de error
            
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
                        % (i)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            self.checkExcelRep("riesgos", risk, risk_to_create, self, form, i)
            self.checkDB("riesgos", risk, Risk, self, form)
            self.checkMaster("riesgos", "riesgo maestro", risk, risk_master_to_create, RiskMaster, "risk_master_ref", self, form)

            risk_to_create.append(risk)

        # Controles
        control_sheet = wb['Controls']
        control_to_create = []
        rows = control_sheet.rows
        
        for i, row in enumerate(rows):
            control = {}

            # if row[0].value is None:
            #     break 

            if row[0].value is not None:
                control['risk_refs'] = row[0].value.replace(' ', '').upper().split(',')
            else:
                control['risk_refs'] = []

            if row[1].value is not None:
                control['sub_process_refs'] = row[1].value.replace(' ', '').upper().split(',')
            else:
                control['sub_process_refs'] = []
            print(control)
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
            control['is_elc'] = row[19].value

            if control['automation'] == '':
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de controles no ha establecido valor para Control Automation en la fila %s')
                        % (i)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            if control['control_frequency'] not in ('CO','BD', 'DI', '1W', '2W', '1M', '2M', '3T', '6M', '1Y', '2Y', '3Y'):
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de controles no ha establecido valor para Control Frequency en la fila %s')
                        % (i)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            if control['is_gap'] not in ('Y', 'N', '-') or control['assert_existence'] not in ('Y', 'N', '-') or control['assert_completeness'] not in ('Y', 'N', '-') or control['assert_valuation'] not in ('Y', 'N', '-') or control['assert_rights'] not in ('Y', 'N', '-') or control['assert_disclosure'] not in ('Y', 'N', '-') or control['assert_accurancy'] not in ('Y', 'N', '-') or control['assert_froud'] not in ('Y', 'N', '-'):
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de controles no ha establecido valor para alguna celda obligatoria en la fila %s')
                        % (i)
                    ),
                )
                return super(GaImportView, self).form_invalid(form)

            self.checkExcelRep("controles", control, control_to_create, self, form, i)

            control_to_create.append(control)
            print(control)

            print('Ctrls to create', len(control_to_create), control_to_create)

            self.checkDB("controles", control, Control, self, form)
            self.checkMaster("controles", "riesgo", control, risk_to_create, Risk, "risk_ref", self, form)
            #self.checkDB("subproceso", domain_risk, DomainRisk, self, form)

            #self.checkMaster("controles", "subproceso", control, risk_to_create, Risk, "risk_ref", self, form)

            for subprocess_ref in c['sub_process_refs']:

                if SubProcess.objects.filter(ref=subprocess_ref).count() == 0:
                    print(subprocess_ref)
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de controles hay una REF a un subproceso que no existe: %s')
                            % (subprocess_ref)
                        ),
                    )
                    return super(GaImportView, self).form_invalid(form)

        print('Ctrls to create', len(control_to_create), control_to_create)

        # Riesgos Compañías
        risk_sheet = wb['RiskCompany']
        risk_company_to_create = []
        rows = risk_sheet.rows

        for i, row in enumerate(rows):
            risk_company = {}

            if row[0].value is None:
                break #mensaje de error

            risk_company['risk_ref'] = row[0].value.strip().replace(' ', '').upper()
            risk_company['company_ref'] = row[1].value.strip().replace(' ', '').upper()
            risk_company['name'] = row[2].value
            risk_company['description'] = row[3].value
            risk_company['krm_activity_affected'] = row[4].value
            risk_company['krm_main_events'] = row[5].value
            risk_company['krm_exposed_staff'] = row[6].value
            risk_company['krm_main_elements'] = row[7].value

            #self.checkExcelRep("riesgo compañía", risk_company, risk_company_to_create, self, form, i)
            self.checkDB("riesgos compañía", risk_company, Risk, self, form)
            self.checkMaster("riesgos compañía", "riesgo", risk, risk_to_create, Risk, "risk_ref", self, form)
            self.checkMaster("riesgos compañía", "compañía", risk, risk_to_create, Company, "company_ref", self, form)

            risk_company_to_create.append(risk_company)
    
        # Control-Compañías
        control_company_sheet = wb['ControlCompany']
        control_company_to_create = []
        rows = control_company_sheet.rows

        for i, row in enumerate(rows):
            control_company = {}

            if row[0].value is None or row[1].value is None:
                break #mensaje de error

            control_company['control_ref'] = row[0].value.strip().replace(' ', '').upper()
            control_company['company_ref'] = row[1].value.strip().replace(' ', '').upper()

            self.checkDB("control compañía", control_company, Company, self, form)
            self.checkMaster("control compañía", "compañía", control_company, control_company_to_create, Company, "company_ref", self, form)

            control_company_to_create.append(control_company)

        print("All checks went good, loading in DB")
        print("Domain", len(domain_risk_to_create))
        print("RMaster", len(risk_master_to_create))
        print("R2", len(risk_to_create))
        print("Ctrls", len(control_to_create))
        print("RiskCompany", len(risk_company_to_create))
        print("CtrlCompany", len(control_company_to_create))
       
        # Vamos a crear cosas
        dr_created, n = 0, len(domain_risk_to_create)
        for i,dr in enumerate(domain_risk_to_create):
            print("DomainRisk %d/%d" % (i, n))
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

        rm_created, n = 0, len(risk_master_to_create)
        for i,rm in enumerate(risk_master_to_create):
            print("RiskMaster %d/%d" % (i, n))
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

        r_created, n = 0, len(risk_to_create)
        for i,r in enumerate(risk_to_create):
            print("Risk %d/%d" % (i, n))
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

        c_created, n = 0, len(control_to_create)
        for i,r in enumerate(control_to_create):
            print("Control %d/%d" % (i, n))
            key_control = False
            is_elc = False
            if r['key_control'] == 'X' or r['key_control'] == 'x':
                key_control = True
            if r['is_elc'] == 'X' or r['key_control'] == 'x':
                is_elc = True
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
                is_elc = is_elc,
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
        risk_company_created, n = 0, len(risk_company_to_create)
        for i,rc in enumerate(risk_company_to_create):
            print("RiskCompany %d/%d" % (i, n))
            rc_object = RiskCompany.objects.get(
                company__ref=rc['company_ref'],
                risk__ref=rc['risk_ref']
            )
            rc_object.active = True

            if rc['name'] != '':
                rc_object.name = rc['name']
            if rc['description'] != '':
                rc_object.description = rc['description']
            if rc['krm_activity_affected'] != '':
                rc_object.krm_activity_affected = rc['krm_activity_affected']
            if rc['krm_main_events'] != '':
                rc_object.krm_main_events = rc['krm_main_events']
            if rc['krm_exposed_staff'] != '':
                rc_object.krm_exposed_staff = rc['krm_exposed_staff']
            if rc['krm_main_elements'] != '':
                rc_object.krm_main_elements = rc['krm_main_elements']

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

        # ControlCompany
        control_company_created, n = 0, len(control_company_to_create)
        for i,cc in enumerate(control_company_to_create):
            print("ControlCompany %d/%d" % (i, n))
            company = Company.objects.get(ref=cc['company_ref'])
            control = Control.objects.get(ref=cc['control_ref'])

            company.controls.add(control)
            control_company_created += 1

        if control_company_created > 0:
            messages.add_message(
                self.request,
                messages.SUCCESS,
                (
                    _(
                        "{0} Controles asociados a compañías creados"
                    ).format(
                        control_company_created,
                    )
                ),
            )

        return super(GaImportView, self).form_valid(form)

    def get_success_url(self):

        return reverse_lazy("configuration:ga_import")
