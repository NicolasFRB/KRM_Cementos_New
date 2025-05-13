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
    RiskCompany,
)

from krm.controls.models import Control
from krm.companies.models import CompanyControls

from krm.process.models import (
    SubProcess,
    Process
)

from krm.evaluations_krm.models import (EvaluationKrmInherent, RiskTestInherent, EvaluationKrmResidual, RiskTestResidual)

from krm.users.decorators import (
    is_global_admin,
    user_can_edit_company,
    user_can_edit_domain_risk_evaluator
)

@method_decorator([login_required, is_global_admin], name='dispatch')
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


@method_decorator([login_required, is_global_admin], name='dispatch')
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


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaImportEvalView(FormView):
    template_name = 'configuration/GaImportEval.html'
    form_class = ImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Importador Evaluaciones')},
        ]
        context['page_title'] = _('Importador de Evaluaciones de Riesgo Finalizadas')
        context['breadcrums'] = breadcrums
        return context

    def checkMandatory(self, name, elem, index, field_key):
        """
        Función auxiliar empleada para verificar que los campos obligatorios de un objeto han sido escritos en
        la template de importación.

        Parameters
        ------------
        name: String.
            Nombre del objeto del cual se quiere crear una instancia con una referencia repetida.
        elem: dict.
            Diccionario de python que contiene los valores de los atributos de la nueva instancia del objeto que queremos crear y para el cual
            estamos realizando esta validación.
        form: Form.
            Formulario ya validado asociado a la vista.
        index: int.
            Número entero que nos indica la fila en la que se encuentra el error de referencia repetida que será la de número index+1.
        field_key: String.
            Nombre del atributo cuya existencia se quiere contrastar.

        """
        problem = False
        if elem[field_key] is None or elem[field_key].strip() == '':
            self.errors_found +=1
            messages.add_message(
                self.request,
                messages.ERROR,
                (_('En la hoja de %s hay un campo obligatorio (*) sin completar en la fila %d') % (name, index)),
            )
            problem = True
        return problem

    def checkExcelRep(self, name, elem, elems_to_create, index, field_key, second_field= None):
        """
        Función empleada para contrastar que no existe una instancia de un objeto con el mismo valor para
        el atributo field_key en la importación de datos, que suele tratarse del atributo referencia del objeto, dado
        que este funciona como identificador de la instancia. Es decir, se contrasta que no existen dos instancias en
        una pestaña de importación que contengan el mismo valor como identificador, no se hace un checkeo con la base de datos
        ya existente.

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
        problem = False
        if second_field:
            for e in elems_to_create:
                if e[field_key] == elem[field_key] and e[second_field] == elem[second_field]:
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de %s hay dos instancias con los campos %s y %s repetidos (fila %d)')
                            % (name, e[field_key], e[second_field], index)
                        ),
                    )
                    problem= True
        else:
            for e in elems_to_create:
                if e[field_key] == elem[field_key]:
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de %s hay una referencia repetida: %s en la fila %d')
                            % (name, e[field_key], index)
                        ),
                    )
                    problem= True
        return problem

    def checkDB(self, name, elem, DBreference, field_key):
        """
        Función que contrasta si existen previamente en la base de datos instancias de un objeto con el mismo identificador que alguna
        de las nuevas instancias que se pretende crear.

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
        if DBreference.objects.filter(ref=elem[field_key]).count() > 0:
            self.errors_found += 1
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('En la hoja de %s hay una referencia que ya existe: %s')
                    % (name, elem[field_key])
                ),
            )
            problem= True
        return problem

    def checkMaster(self, name, master_name, elem, master_DBreference, master):
        exist = False
        if master_DBreference.objects.filter(ref=elem[master]).count() > 0:
            exist= True
        if not exist:
          self.errors_found += 1
          messages.add_message(
              self.request,
              messages.ERROR,
              (
                  _('En la hoja de %s la referencia %s de %s no existe') % (name, elem[master], master_name)
              ),
            )
        problem = not exist
        return problem

    def checkAdministrator(self, name, master_company, useremail):
        problem= False
        if User.objects.filter(email=useremail).count() == 1:
            administrator = User.objects.get(email=useremail)
            company = Company.objects.get(ref=master_company) #se podría dar el caso también de que la compañía introducida no existiese (saltaría antes, pero condicional para ejecutar)

            if company not in administrator.companies_admin.all():
                self.errors_found += 1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('El usuario %s insertado en la pestaña de %s no es administrador de la compañía %s') % (useremail, name, company.name)
                    ),
                )
                problem= True
        else:
            self.errors_found += 1
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('No existe ningún usuario que tenga la siguiente dirección de email: %s ') % (useremail)
                ),
            )
            problem = True
        return problem

    def checkEvaluator(self, name, master_company, useremail):
        problem= False
        if User.objects.filter(email=useremail).count() == 1:
            administrator = User.objects.get(email=useremail)
            company = Company.objects.get(ref=master_company) #se podría dar el caso también de que la compañía introducida no existiese (saltaría antes, pero condicional para ejecutar)

            if company not in administrator.companies.all():
                self.errors_found += 1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('El usuario %s insertado en la pestaña de %s no es usuario de la compañía %s') % (useremail, name, company.name)
                    ),
                )
                problem= True
        else:
            self.errors_found += 1
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('No existe ningún usuario que tenga la siguiente dirección de email: %s ') % (useremail)
                ),
            )
            problem = True
        return problem

    def checkRiskCompany(self, name, risk_ref, company_ref, index):
        problem= False
        if Risk.objects.filter(ref= risk_ref).count() == 0:
            self.errors_found +=1
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('En la pestaña %s la referencia del riesgo introducida en la fila %d no existe') % (name, index)
                ),
            )
            problem = True

        else:
            riesgo, compania= Risk.objects.get(ref = risk_ref), Company.objects.get(ref= company_ref)
            if RiskCompany.objects.filter(risk= riesgo, company= compania).count() == 0:
                self.errors_found +=1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la pestaña %s el riesgo de compañía introducido en la fila %d no existe') % (name, index)
                    ),
                )
                problem = True
        return problem


    def form_valid(self, form):
        input_excel = self.request.FILES['data_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)
        self.errors_found = 0

        #Evaluaciones inherentes
        evaluation_krm_inherent_sheet = wb['Inherent Evaluations']
        evaluation_krm_inherent_to_create = []
        inherent_company= {}
        rows = [row for row in evaluation_krm_inherent_sheet.iter_rows() if any(cell.value is not None and str(cell.value).strip()!= '' for cell in row)]
        for row in rows:
            i = row[0].row
            if not i == 1:
                ev_inherent = {}
                ev_inherent['ref'] = row[0].value
                ev_inherent['company'] = row[1].value.strip()
                ev_inherent['description'] = row[2].value
                ev_inherent['date_begin'] = row[3].value
                ev_inherent['date_end'] = row[4].value
                ev_inherent['certification_year'] = row[5].value if row[5].value else datetime.date.today().year #hemos añadido esto en el caso de que se inserte un valor vacío
                ev_inherent['certification_period'] = row[6].value
                ev_inherent['admin_supervisor'] = row[7].value

                #comprobaciones correspondientes a la referencia de la evaluación
                if self.checkMandatory(_("evaluaciones de riesgo inherente"), ev_inherent, i, "ref"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkExcelRep(_("evaluaciones de riesgo inherente"), ev_inherent, evaluation_krm_inherent_to_create, i, "ref"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkDB(_("evaluaciones de riesgo inherente"), ev_inherent, EvaluationKrmInherent, "ref"):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones correspondientes a la compañía de la evaluación
                if self.checkMandatory(_("evaluaciones de riesgo inherente"), ev_inherent, i, "company"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkMaster(_("evaluaciones de riesgo inherente"), _("compañía"), ev_inherent, Company, "company"):
                    return super(GaImportEvalView, self).form_invalid(form)
                inherent_company[ev_inherent['ref']] = ev_inherent['company'] #una vez se han comprobado evaluación-compañía añadimos al diccionario

                #comprobaciones correspondientes a las fechas de la evaluación
                if ev_inherent['date_begin'] is None or ev_inherent['date_end'] is None:
                    self.errors_found +=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la hoja de evaluaciones de riesgo inherente hay un campo obligatorio (*) sin completar en la fila %d') % (i)),
                    )
                    return super(GaImportEvalView, self).form_invalid(form)

                if ev_inherent['date_end'] < ev_inherent['date_begin']:
                    self.errors_found +=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la pestaña de evaluaciones de riesgo inherente en la fila %d las fechas de inicio y fin son incongruentes') % (i)
                        )
                    )
                    return super(GaImportEvalView, self).form_invalid(form)

                if row[5].value:
                    if row[5].value not in range(2000, datetime.date.today().year + 1):
                        self.errors_found +=1
                        messages.add_message(self.request, messages.ERROR,
                                             (
                                                 _('En la pestaña de evaluaciones de riesgo residual el valor de año certificación de la fila %d no es válido') % (i)
                                             )
                        )
                        return super(GaImportEvalView, self).form_invalid(form)

                #comprobación del administrador de compañía
                if self.checkMandatory(_("evaluaciones de riesgo inherente"), ev_inherent, i, "admin_supervisor"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkAdministrator(_("evaluaciones de riesgo residual"), ev_inherent['company'], ev_inherent['admin_supervisor']):
                    return super(GaImportEvalView, self).form_invalid(form)

                evaluation_krm_inherent_to_create.append(ev_inherent)

        #Tests de riesgo inherentes
        risk_test_inherent_sheet = wb['Inherent Risk Tests']
        risk_test_inherent_to_create = []
        inherentes_testpage = []
        rows = [row for row in risk_test_inherent_sheet.iter_rows() if any(cell.value is not None and str(cell.value).strip()!= '' for cell in row)]
        for row in rows:
            i = row[0].row
            if not i == 1:

                risk_inherent = {}
                risk_inherent['evaluation'] = row[0].value
                risk_inherent['risk'] = row[1].value
                risk_inherent['expert'] = row[2].value
                risk_inherent['impact_reputational_level_expert'] = row[3].value
                risk_inherent['impact_economic_level_expert'] = row[4].value
                risk_inherent['impact_regulatory_level_expert'] = row[5].value
                risk_inherent['impact_objectives_level_expert'] = row[6].value
                risk_inherent['impact_dedication_level_expert'] = row[7].value
                risk_inherent['probability_level_expert'] = row[8].value
                risk_inherent['event_speed_level_expert'] = row[9].value
                risk_inherent['description_expert'] = row[10].value
                risk_inherent['impact_level_administrator'] = row[11].value
                risk_inherent['probability_level_administrator'] = row[12].value
                risk_inherent['event_speed_level_administrator'] = row[13].value
                risk_inherent['description_administrator'] = row[14].value

                #comprobaciones de la evaluación del test de riesgo
                if self.checkMandatory(_("tests de riesgo inherente"), risk_inherent, i, "evaluation"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if risk_inherent['evaluation'] not in inherent_company.keys():
                    self.errors_found +=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la pestaña de tests de riesgo inherente la fila %d contiene una referencia a una evaluación no existente en la pestaña previa') % (i)
                        )
                    )
                    return super(GaImportEvalView, self).form_invalid(form)
                if risk_inherent['evaluation'] not in inherentes_testpage: #almacenamos la evaluación para la comprobación posterior de que todas las evaluaciones tengan al menos un test de riesgo
                    inherentes_testpage.append(risk_inherent['evaluation'])

                #comprobaciones correspondientes al riesgo N2 introducido:
                if self.checkMandatory(_("tests de riesgo inherente"), risk_inherent, i, "risk"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkRiskCompany(_("tests de riesgo inherente"), risk_inherent['risk'], inherent_company[risk_inherent['evaluation']], i):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobación de repetición:
                if self.checkExcelRep(_("tests de riesgo inherente"), risk_inherent, risk_test_inherent_to_create, i, "evaluation", "risk"):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones correspondientes al evaluador del riesgo:
                if self.checkMandatory(_("tests de riesgo inherente"), risk_inherent, i, "expert"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkEvaluator(_("tests de riesgo inherente"), inherent_company[risk_inherent['evaluation']], risk_inherent['expert']):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones valoraciones evaluador
                if risk_inherent['impact_reputational_level_expert'] not in range(1, 6) or risk_inherent['impact_economic_level_expert'] not in range(1, 6) or risk_inherent['impact_regulatory_level_expert'] not in range(1, 6) or risk_inherent['impact_objectives_level_expert'] not in range(1, 6) or risk_inherent['impact_dedication_level_expert'] not in range(1, 6) or risk_inherent['probability_level_expert'] not in range(1, 6) or risk_inherent['event_speed_level_expert'] not in range(1,6):
                    self.errors_found +=1
                    messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la pestaña de tests de riesgo inherente la fila %d contiene una valoración por parte del evaluador fuera del rango aceptado [1, 5]') % (i)
                            )
                        )
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones valoraciones administrador
                if risk_inherent['impact_level_administrator'] not in range(1, 6) or risk_inherent['probability_level_administrator'] not in range(1, 6) or risk_inherent['event_speed_level_administrator'] not in range(1, 6):
                    self.errors_found +=1
                    messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la pestaña de tests de riesgo inherente la fila %d contiene una valoración por parte del administrador fuera del rango aceptado [1, 5]') % (i)
                            )
                        )
                    return super(GaImportEvalView, self).form_invalid(form)

                risk_test_inherent_to_create.append(risk_inherent)

        #comprobación evaluaciones sin test de riesgo:
        for inherent_evaluation in inherent_company.keys():
            if inherent_evaluation not in inherentes_testpage:
                self.errors_found +=1
                messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la pestaña de evaluaciones de riesgo inherente no se está importando ningún test de riesgo para la evaluación %s. No es posible crear evaluaciones vacías.') % (i)
                            )
                        )
                return super(GaImportEvalView, self).form_invalid(form)

        #Evaluaciones residuales
        evaluation_krm_residual_sheet = wb['Residual Evaluations']
        evaluation_krm_residual_to_create = []
        residual_company = {}
        rows = [row for row in evaluation_krm_residual_sheet.iter_rows() if any(cell.value is not None and str(cell.value).strip()!= '' for cell in row)]
        for row in rows:
            i = row[0].row
            if not i == 1:

                evaluacion, compania = False, False
                ev_residual = {}
                ev_residual['ref'] = row[0].value
                ev_residual['company'] = row[1].value.strip()
                ev_residual['description'] = row[2].value
                ev_residual['date_begin'] = row[3].value
                ev_residual['date_end'] = row[4].value
                ev_residual['certification_year'] = row[5].value if row[5].value else datetime.date.today().year #hemos añadido esto en el caso de que se inserte un valor vacío
                ev_residual['certification_period'] = row[6].value
                ev_residual['admin_supervisor'] = row[7].value

                #comprobaciones correspondientes a la referencia de la evaluación
                if self.checkMandatory(_("evaluaciones de riesgo residual"), ev_residual, i, "ref"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkExcelRep(_("evaluaciones de riesgo residual"), ev_residual, evaluation_krm_residual_to_create, i, "ref"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkDB(_("evaluaciones de riesgo residual"), ev_residual, EvaluationKrmResidual, "ref"):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones correspondientes a la compañía de la evaluación
                if self.checkMandatory(_("evaluaciones de riesgo residual"), ev_residual, i, "company"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkMaster(_("compañía"), _("evaluaciones de riesgo residual"), ev_residual, Company, "company"):
                    return super(GaImportEvalView, self).form_invalid(form)
                residual_company[ev_residual['ref']] = ev_residual['company']

                #comprobaciones correspondientes a las fechas de la evaluación
                if ev_residual['date_begin'] is None or ev_residual['date_end'] is None:
                    self.errors_found +=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la hoja de evaluaciones de riesgo residual hay un campo obligatorio (*) sin completar en la fila %d') % (i)),
                    )
                    return super(GaImportEvalView, self).form_invalid(form)

                if ev_residual['date_end'] < ev_residual['date_begin']:
                    self.errors_found +=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la pestaña de evaluaciones de riesgo residual en la fila %d las fechas de inicio y fin son incongruentes') % (i)
                        )
                    )
                    return super(GaImportEvalView, self).form_invalid(form)

                if row[5].value:
                    if row[5].value not in range(2000, datetime.date.today().year + 1):
                        self.errors_found +=1
                        messages.add_message(self.request, messages.ERROR,
                                             (
                                                 _('En la pestaña de evaluaciones de riesgo residual el valor de año certificación de la fila %d no es válido') % (i)
                                             )
                        )
                        return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones del administrador de compañía:
                if self.checkMandatory(_("evaluaciones de riesgo residual"), ev_residual, i, "admin_supervisor"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkAdministrator(_("evaluaciones de riesgo residual"), ev_residual['company'], ev_residual['admin_supervisor']):
                    return super(GaImportEvalView, self).form_invalid(form)

                evaluation_krm_residual_to_create.append(ev_residual)

        #Tests de riesgo residuales
        risk_test_residual_sheet = wb['Residual Risk Tests']
        risk_test_residual_to_create = []
        residuales_testpage= [] #lista creada para almacenar todas evaluaciones a las que se le añaden tests de riesgo
        rows = [row for row in risk_test_residual_sheet.iter_rows() if any(cell.value is not None and str(cell.value).strip()!= '' for cell in row)]
        for row in rows:
            i = row[0].row
            if not i == 1:

                risk_residual = {}
                risk_residual['evaluation'] = row[0].value
                risk_residual['risk'] = row[1].value
                risk_residual['evaluator'] = row[2].value
                risk_residual['impact_reputational_level_evaluator'] = row[3].value
                risk_residual['impact_economic_level_evaluator'] = row[4].value
                risk_residual['impact_regulatory_level_evaluator'] = row[5].value
                risk_residual['impact_objectives_level_evaluator'] = row[6].value
                risk_residual['impact_dedication_level_evaluator'] = row[7].value
                risk_residual['probability_level_evaluator'] = row[8].value
                risk_residual['event_speed_level_evaluator'] = row[9].value
                risk_residual['description_evaluator'] = row[10].value
                risk_residual['impact_level_administrator'] = row[11].value
                risk_residual['probability_level_administrator'] = row[12].value
                risk_residual['event_speed_level_administrator'] = row[13].value
                risk_residual['description_administrator'] = row[14].value

                #comprobaciones de la evaluación del test de riesgo:
                if self.checkMandatory(_("tests de riesgo residual"), risk_residual, i, "evaluation"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if risk_residual['evaluation'] not in residual_company.keys():
                    self.errors_found +=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la pestaña de tests de riesgo residual la fila %d contiene una referencia a una evaluación no existente en la pestaña previa') % (i)
                        )
                    )
                    return super(GaImportEvalView, self).form_invalid(form)

                if risk_residual['evaluation'] not in residuales_testpage:
                    residuales_testpage.append(risk_residual['evaluation'])

                #comprobaciones correspondientes al riesgo N2 introducido:
                if self.checkMandatory(_("tests de riesgo residual"), risk_residual, i, "risk"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkRiskCompany(_("tests de riesgo residual"), risk_residual['risk'], residual_company[risk_residual['evaluation']], i):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobación de repetición:
                if self.checkExcelRep(_("tests de riesgo residual"), risk_residual, risk_test_residual_to_create, i, "evaluation", "risk"):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones correspondientes al evaluador de riesgo:
                if self.checkMandatory(_("tests de riesgo residual"), risk_residual, i, "evaluator"):
                    return super(GaImportEvalView, self).form_invalid(form)
                if self.checkEvaluator(_("tests de riesgo residual"), residual_company[risk_residual['evaluation']], risk_residual['evaluator']):
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones valoraciones evaluador
                if risk_residual['impact_reputational_level_evaluator'] not in range(1, 6) or risk_residual['impact_economic_level_evaluator'] not in range(1, 6) or risk_residual['impact_regulatory_level_evaluator'] not in range(1, 6) or risk_residual['impact_objectives_level_evaluator'] not in range(1, 6) or risk_residual['impact_dedication_level_evaluator'] not in range(1, 6) or risk_residual['probability_level_evaluator'] not in range(1, 6) or risk_residual['event_speed_level_evaluator'] not in range(1, 6):
                    self.errors_found +=1
                    messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la pestaña de tests de riesgo residual la fila %d contiene una valoración por parte del evaluador fuera del rango aceptado [1, 5]') % (i)
                            )
                        )
                    return super(GaImportEvalView, self).form_invalid(form)

                #comprobaciones valoraciones administrador
                if risk_residual['impact_level_administrator'] not in range(1, 6) or risk_residual['probability_level_administrator'] not in range(1, 6) or risk_residual['event_speed_level_administrator'] not in range(1, 6):
                    self.errors_found +=1
                    messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la pestaña de tests de riesgo residual la fila %d contiene una valoración por parte del administrador fuera del rango aceptado [1, 5]') % (i)
                            )
                        )
                    return super(GaImportEvalView, self).form_invalid(form)

                risk_test_residual_to_create.append(risk_residual)

        for residual_evaluation in residual_company.keys():
            if residual_evaluation not in residuales_testpage:
                self.errors_found +=1
                messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la pestaña de evaluaciones de riesgo residual no se está importando ningún test de riesgo para la evaluación %s. No es posible crear evaluaciones vacías.') % (i)
                            )
                        )
                return super(GaImportEvalView, self).form_invalid(form)


        #Creamos los elementos en caso de que no haya habido errores
        if self.errors_found == 0:

            ie_created= 0
            for evaluation in evaluation_krm_inherent_to_create:
                EvaluationKrmInherent.objects.create(
                    ref= evaluation['ref'],
                    company= Company.objects.get(ref = evaluation['company']),
                    description= evaluation['description'],
                    date_begin= evaluation['date_begin'],
                    date_end= evaluation['date_end'],
                    certification_year= int(evaluation['certification_year']),
                    certification_period= evaluation['certification_period'],
                    status= "FI",
                    admin_supervisor= User.objects.get(email = evaluation['admin_supervisor'])
                )
                ie_created += 1

            if ie_created > 0:
                messages.add_message(self.request, messages.SUCCESS,
                    (
                        _("{0} Evaluaciones de riesgo inherente importadas").format(ie_created)
                    ),
                )

            it_created = 0
            for rt in risk_test_inherent_to_create:
                RiskTestInherent.objects.create(
                    evaluation=EvaluationKrmInherent.objects.get(ref = rt['evaluation']),
                    risk=RiskCompany.objects.get(
                        company__ref= inherent_company[rt['evaluation']],
                        risk__ref= rt['risk']
                    ),
                    expert=User.objects.get(email = rt['expert']), #parece ser que el usuario hay que darlo a través de su mail
                    impact_economic_expert= int(rt['impact_economic_level_expert']),
                    impact_objectives_expert= int(rt['impact_objectives_level_expert']),
                    impact_reputational_expert= int(rt['impact_reputational_level_expert']),
                    impact_regulatory_expert= int(rt['impact_regulatory_level_expert']),
                    impact_dedication_expert= int(rt['impact_dedication_level_expert']),
                    probability_level_expert= int(rt['probability_level_expert']),
                    event_speed_level_expert= int(rt['event_speed_level_expert']),
                    impact_level_administrator= int(rt['impact_level_administrator']),
                    probability_level_administrator= int(rt['probability_level_administrator']),
                    event_speed_level_administrator= int(rt['event_speed_level_administrator']),
                    status= 3,
                    description_expert= rt['description_expert'],
                    description_administrator= rt['description_administrator']
                )

                it_created +=1

            if it_created > 0:
                messages.add_message(self.request, messages.SUCCESS,
                    (
                        _("{0} Tests de riesgo inherente importados").format(it_created)
                    ),
                )

            re_created= 0
            for evaluation in evaluation_krm_residual_to_create:
                EvaluationKrmResidual.objects.create(
                ref= evaluation['ref'],
                company= Company.objects.get(ref = evaluation['company']),
                description= evaluation['description'],
                date_begin= evaluation['date_begin'],
                date_end= evaluation['date_end'],
                certification_year= int(evaluation['certification_year']),
                certification_period= evaluation['certification_period'],
                status= "FI",
                admin_supervisor= User.objects.get(email = evaluation['admin_supervisor'])
                )
                re_created += 1

            if re_created > 0:
                messages.add_message(self.request, messages.SUCCESS,
                    (
                        _("{0} Evaluaciones de riesgo residual importadas").format(re_created)
                    ),
                )

            rt_created = 0
            for rt in risk_test_residual_to_create:
                RiskTestResidual.objects.create(
                    evaluation=EvaluationKrmInherent.objects.get(ref = rt['evaluation']),
                    risk=RiskCompany.objects.get(company__ref= residual_company[rt['evaluation']], risk__ref= rt['risk']),
                    expert=User.objects.get(email = rt['evaluator']),
                    impact_economic_evaluator= int(rt['impact_economic_level_evaluator']),
                    impact_objectives_evaluator= int(rt['impact_objectives_level_evaluator']),
                    impact_reputational_evaluator= int(rt['impact_reputational_level_evaluator']),
                    impact_regulatory_evaluator= int(rt['impact_regulatory_level_evaluator']),
                    impact_dedication_evaluator= int(rt['impact_dedication_level_evaluator']),
                    probability_level_evaluator= int(rt['probability_level_evaluator']),
                    event_speed_level_evaluator= int(rt['event_speed_level_evaluator']),
                    impact_level_administrator= int(rt['impact_level_administrator']),
                    probability_level_administrator= int(rt['probability_level_administrator']),
                    event_speed_level_administrator= int(rt['event_speed_level_administrator']),
                    status= 3,
                    description_evaluator= rt['description_evaluator'],
                    description_administrator= rt['description_administrator']
                )

                rt_created +=1

            if rt_created > 0:
                messages.add_message(self.request, messages.SUCCESS,
                    (
                        _("{0} Tests de riesgo residual importados").format(rt_created)
                    ),
                )

        return super(GaImportEvalView, self).form_valid(form)

    def get_success_url(self):

        return reverse_lazy("configuration:ga_import_eval")

@method_decorator([login_required, is_global_admin], name='dispatch')
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

    def checkMandatory(self, name, elem, index, field_key):
        """
        Función auxiliar empleada para verificar que los campos obligatorios de un objeto han sido escritos en
        la template de importación.

        Parameters
        ------------
        name: String.
            Nombre del objeto del cual se quiere crear una instancia con una referencia repetida.
        elem: dict.
            Diccionario de python que contiene los valores de los atributos de la nueva instancia del objeto que queremos crear y para el cual
            estamos realizando esta validación.
        form: Form.
            Formulario ya validado asociado a la vista.
        index: int.
            Número entero que nos indica la fila en la que se encuentra el error de referencia repetida que será la de número index+1.
        field_key: String.
            Nombre del atributo cuya existencia se quiere contrastar.

        """
        problem = False
        if elem[field_key] in (None, ''):
            self.errors_found+=1
            messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de %(name)s hay un campo obligatorio (*) sin completar en la fila %(index)d') % {
                        "name": name,
                        "index": index
                        }
                )
            )
            problem= True
        return problem


    def checkExcelRep(self, name, elem, elems_to_create, index, field_key):
        """
        Función empleada para contrastar que no existe una instancia de un objeto con el mismo valor para
        el atributo field_key en la importación de datos, que suele tratarse del atributo referencia de un dato maestro, dado
        que este funciona como identificador de la instancia. Es decir, se contrasta que no existen dos instancias en
        una pestaña de importación que contengan el mismo valor como identificador, no se hace un checkeo con la base de datos
        ya existente.

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
                self.errors_found += 1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de %(name)s hay una referencia repetida: %(value)s en la fila %(index)d') % {
                            "name": name,
                            "value": e[field_key],
                            "index": index
                        }
                    ),
                )
                problem= True
        return problem

    def checkDB(self, name, elem, DBreference, field_key):
        """
        Función que contrasta si existen previamente en la base de datos instancias de un objeto con el mismo identificador que alguna
        de las nuevas instancias que se pretende crear.

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
        if DBreference.objects.filter(ref=elem[field_key]).count() > 0:
            self.errors_found += 1
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('En la hoja de %(name)s hay una referencia que ya existe: %(value)s') % {
                        "name": name,
                        "value": elem[field_key]
                    }
                ),
            )
            problem = True
        return problem

    def checkCompanyObjects(self, name, elem, masters_to_create):
        """
        Función creada para validar la existencia de los maestros a los que hace referencia el elemento de compañía. En el caso de
        un control de compañía, dado que el usuario quiere activarlo, hemos de verificar que tanto la compañía introducida como el control
        existen bien en la base de datos, bien se han creado a través del propio importador. Puesto que las compañías no se importan, solo
        verificamos su existencia en la base de datos.

        Parameters
        -----------
        name: String.
            Nombre del tipo de elemento de compañía cuya validación vamos a realizar (control o riesgo de compañía).
        elem: dict.
            Diccionario que contiene los datos de la instancia riesgo/control de compañía.
        masters_to_create: list.
            Lista de diccionarios con todos los riesgos/controles maestros de las pestañas correspondientes que se van a crear.
        form: Form.
            Formulario validado previamente.

        """
        problem = False
        if name == "riesgos de compañía":
            master_exists= Risk.objects.filter(ref= elem['risk_ref']).exists()
            company_exists= Company.objects.filter(ref= elem['company_ref']).exists()
            if not master_exists:
                for risk in masters_to_create:
                    if risk['ref'] == elem['risk_ref']:
                        master_exists= True
            if not master_exists or not company_exists:
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de %s hay filas que contienen referencias a riesgos (%s) o compañías (%s) no existentes')
                            % (name, elem['risk_ref'], elem['company_ref'])
                        ),
                    )
                    problem= True
        else:
            master_exists= Control.objects.filter(ref= elem['control_ref']).exists()
            company_exists= Company.objects.filter(ref= elem['company_ref']).exists()
            if not master_exists:
                for control in masters_to_create:
                    if control['ref'] == elem['control_ref']:
                        master_exists= True
            if not master_exists or not company_exists:
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de %s hay filas que contienen referencias a controles (%s) o compañías (%s) no existentes')
                            % (name, elem['control_ref'], elem['company_ref'])
                        ),
                    )
                    problem= True
        return problem


    def checkMaster(self, name, master_name, elem, elems_to_create, master_DBreference, master):
        """
        Función que contrasta la existencia de un dato maestro con el identificador indicado para su asociación
        a otro tipo de dato maestro, puesto que no se deben crear instancias de objetos con referencias a otras instancias
        de otro objeto no existentes.

        Parameters
        -----------
        name: String.
            Nombre del objeto del cual se quiere crear una instancia con una referencia a su maestro no existente.
        master_name: String.
            Nombre del objeto maestro asociado cuya referencia es inexistente.
        elem: dict.
            Diccionario con los datos de la instancia que se quiere crear.
        elems_to_create: list.
            Lista que contiene los diccionarios respectivos a instancias de maestros que se quieren importar desde el excel.
        master_DB_reference: object.
            Objeto maestro cuya existencia de referencia queremos contrastar.
        master: String.
            Cadena de texto que define el nombre de la llave del diccionario que hace referencia a la referencia del maestro.
        form: Form.
            Formulario validado previamente.

        """
        exist = False
        if master_DBreference.objects.filter(ref=elem[master]).count() > 0:
            exist = True
        else:
            for master_object in elems_to_create:
                if elem[master] == master_object['ref']:
                    exist = True
        problem= not exist
        if problem:
            self.errors_found += 1
            messages.add_message(
                self.request,
                messages.ERROR,
                (
                    _('En la hoja de %(name)s la referencia %(value)s de %(master)s no existe') % {
                        "name": name,
                        "value": elem[master],
                        "master": master_name
                    }
                ),
            )
        return problem

    def check_user_in_company(self, master_company, user_type):
        """
        Función que valida la existencia de usuarios con el email indicado en las columnas de responsables y supervisores dentro
        de la compañía en la cual se quiere crear este control de compañía.

        Parameters
        -----------
        master_company: dict.
            Diccionario de python que contiene los datos del control/riesgo de compañía que se quiere crear.
        user_type: String.
            Cadena de texto que nos especifica si queremos contrastar la existencia de los responsables o de los supervisores.
        form: Form.
            Formulario ya validado.

        """
        problem= False
        for user in master_company[user_type]:
            if User.objects.filter(email=user).count() == 1:
                owner = User.objects.get(email=user)
                company = Company.objects.get(ref=master_company['company_ref'])

                if company not in owner.companies.all():
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('El usuario %s no pertence a la compañia %s')
                            % (owner.email, company.name)
                        ),
                    )
                    problem= True
            else:
                self.errors_found += 1
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('No existe ningún usuario que tenga siguiente dirección de email: %s ') % (user)
                    ),
                )
                problem= True
        return problem

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
        self.errors_found = 0

        # Dominios de Riesgo
        domain_risk_sheet = wb['Domain Risks']
        domain_risk_to_create = []
        rows = [row for row in domain_risk_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                domain_risk = {}

                domain_risk['ref'] = row[0].value.strip() if row[0].value else row[0].value
                domain_risk['name'] = row[1].value
                domain_risk['description'] = row[2].value

                #comprobaciones correspondientes a la referencia
                if self.checkMandatory(_("dominios de riesgo"), domain_risk, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkExcelRep(_("dominios de riesgo"), domain_risk, domain_risk_to_create, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkDB(_("dominios de riesgo"), domain_risk, DomainRisk, "ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobaciones correspondientes al nombre:
                if self.checkMandatory(_("dominios de riesgo"), domain_risk, i, "name"):
                    return super(GaImportView, self).form_invalid(form)
                #comprobaciones correspondientes a la descripción
                if self.checkMandatory(_("dominios de riesgo"), domain_risk, i, "description"):
                    return super(GaImportView, self).form_invalid(form)

                domain_risk_to_create.append(domain_risk)

        # Riesgos Maestros
        risk_master_sheet = wb['Master Risks N1']
        risk_master_to_create = []
        rows = [row for row in risk_master_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                risk_master = {}

                risk_master['domain_risk_ref'] = row[0].value.strip() if row[0].value else row[0].value
                risk_master['ref'] = row[1].value.strip() if row[1].value else row[1].value
                risk_master['name'] = row[2].value
                risk_master['description'] = row[3].value

                #comprobaciones correspondientes a la referencia de dominio de riesgo:
                if self.checkMandatory(_("riesgos maestros"), risk_master, i, "domain_risk_ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkMaster(_("riesgos maestros"), _("dominios de riesgo"), risk_master, domain_risk_to_create, DomainRisk, "domain_risk_ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobaciones correspondientes a la referencia del riesgo maestro:
                if self.checkMandatory(_("riesgos maestros"), risk_master, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkExcelRep(_("riesgos maestros"), risk_master, risk_master_to_create, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkDB(_("riesgos maestros"), risk_master, RiskMaster, "ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobación correspondiente al nombre del riesgo maestro:
                if self.checkMandatory(_("riesgos maestros"), risk_master, i, "name"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobación correspondiente a la descripción del riesgo maestro:
                if self.checkMandatory(_("riesgos maestros"), risk_master, i, "description"):
                    return super(GaImportView, self).form_invalid(form)

                risk_master_to_create.append(risk_master)

        # Riesgos
        risk_sheet = wb['Risks N2']
        risk_to_create = []
        rows = [row for row in risk_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                risk = {}

                risk['risk_master_ref'] = row[0].value.strip() if row[0].value else row[0].value
                risk['ref'] = row[1].value.strip() if row[1].value else row[1].value
                risk['name'] = row[2].value
                risk['description'] = row[3].value
                risk['impact_inherent'] = row[4].value
                risk['impact_residual'] = row[5].value
                risk['probability_inherent'] = row[6].value
                risk['probability_residual'] = row[7].value
                risk['event_speed']= row[8].value
                risk['krm_activity_affected'] = row[9].value
                risk['krm_main_events'] = row[10].value
                risk['krm_exposed_staff'] = row[11].value
                risk['krm_main_elements'] = row[12].value

                #comprobaciones de la referencia del riesgo maestro asociado:
                if self.checkMandatory(_("riesgos"), risk, i, "risk_master_ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkMaster(_("riesgos"), _("riesgo maestro"), risk, risk_master_to_create, RiskMaster, "risk_master_ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobaciones de la referencia del riesgo N2:
                if self.checkMandatory(_("riesgos"), risk, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkExcelRep(_("riesgos"), risk, risk_to_create, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkDB(_("riesgos"), risk, Risk, "ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobación del nombre del riesgo N2:
                if self.checkMandatory(_("riesgos"), risk, i, "name"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobamos los campos de valores inherentes/residuales:
                if risk['impact_inherent'] not in range(0, 6) or risk['impact_residual'] not in range(0, 6) or risk['probability_inherent'] not in range(1, 6) or risk['probability_residual'] not in range(1, 6) or risk['event_speed'] not in range(0, 6):
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('El valor numérico de impacto, probabilidad o velocidad de ocurrencia introducido en la fila %d no es válido')% (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                risk_to_create.append(risk)

        #Procesos
        process_sheet = wb['Processes']
        process_to_create = []
        rows = [row for row in process_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                process = {}

                process['ref'] = row[0].value.strip() if row[0].value else row[0].value
                process['name'] = row[1].value
                process['description'] = row[2].value

                #comprobaciones de la referencia del proceso:
                if self.checkMandatory(_("procesos"), process, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkExcelRep(_("procesos"), process, process_to_create, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkDB(_("procesos"), process, Process, "ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobación del nombre del proceso:
                if self.checkMandatory(_("procesos"), process, i, "name"):
                    return super(GaImportView, self).form_invalid(form)

                process_to_create.append(process)

        #Subprocesos
        subprocess_sheet = wb['Subprocesses']
        subprocess_to_create = []
        rows = [row for row in subprocess_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                subprocess = {}

                subprocess['process_master_ref'] = row[0].value.strip() if row[0].value else row[0].value
                subprocess['ref'] = row[1].value.strip() if row[1].value else row[1].value
                subprocess['name'] = row[2].value
                subprocess['description'] = row[3].value

                #comprobaciones correspondientes a la referencia del proceso:
                if self.checkMandatory(_("subprocesos"), process, i, "process_master_ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkMaster(_("subprocesos"), "procesos", subprocess, process_to_create, Process, "process_master_ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobaciones correspondientes a la referencia del subproceso:
                if self.checkMandatory(_("subprocesos"), subprocess, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkExcelRep(_("subprocesos"), subprocess, subprocess_to_create, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkDB(_("subprocesos"), subprocess, SubProcess, "ref"):
                    return super(GaImportView, self).form_invalid(form)

                #comprobación del nombre del subproceso:
                if self.checkMandatory(_("subprocesos"), subprocess, i, "name"):
                    return super(GaImportView, self).form_invalid(form)

                subprocess_to_create.append(subprocess)

        # Controles
        control_sheet = wb['Controls']
        control_to_create = []
        rows = [row for row in control_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                control = {}

                if row[2].value is None:
                    break
                if row[0].value is not None:
                    control['risk_refs'] = row[0].value.strip().split(',')
                else:
                    control['risk_refs'] = []

                if row[1].value is not None:
                    control['sub_process_refs'] = row[1].value.strip().split(',')
                else:
                    control['sub_process_refs'] = []

                control['ref'] = row[2].value.strip() if row[2].value else row[2].value
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
                control['assert_accuracy'] = row[17].value
                control['assert_fraud'] = row[18].value
                control['is_elc'] = row[19].value
                control['evidence'] = row[20].value
                control['scope'] = row[21].value
                control['plant'] = row[22].value

                #comprobaciones correspondientes a las referencias de los riesgos asociados:
                for risk_ref in control['risk_refs']:
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
                            (_('En la hoja de controles hay una REF a un riesgo que no existe: %s') % (risk_ref)),
                        )
                        return super(GaImportView, self).form_invalid(form)

                #comprobaciones correspondientes a las referencias de los subprocesos asociados:
                for subprocess_ref in control['sub_process_refs']:
                    subprocess_exist = False
                    if SubProcess.objects.filter(ref=subprocess_ref).count() > 0:
                        subprocess_exist = True
                    else:
                        for subprocess in subprocess_to_create:
                            if subprocess_ref == subprocess['ref']:
                                subprocess_exist = True
                    if not subprocess_exist:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la hoja de controles hay una REF a un subproceso que no existe: %s')
                                % (subprocess_ref)
                            ),
                        )
                        return super(GaImportView, self).form_invalid(form)

                #comprobaciones correspondientes a la referencia del control:
                if self.checkMandatory(_("controles"), control, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkExcelRep(_("controles"), control, control_to_create, i, "ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkDB(_("controles"), control, Control, "ref"):
                    return super(GaImportView, self).form_invalid(form)

                if control['control_type'] not in ('P', 'D'):
                    self.errors_found+=1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la pestaña de controles no ha establecido un valor válido para Control Type en la fila %s') % (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                if control['automation'] not in ('A', 'M', 'S'):
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la pestaña de controles no ha establecido un valor válido para Control Automation en la fila %s') % (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                if control['control_frequency'] not in ('CO','OD', 'DI', '1W', '2W', '1M', '2M','3T', '4T', '6M', '1Y', '2Y', '3Y', '4Y', '5Y'):
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la pestaña de controles no ha establecido un valor válido para Control Frequency en la fila %s') % (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                if control['is_gap'] not in ('Y', 'N', '-') or control['assert_existence'] not in ('Y', 'N', '-') or control['assert_completeness'] not in ('Y', 'N', '-') or control['assert_valuation'] not in ('Y', 'N', '-') or control['assert_rights'] not in ('Y', 'N', '-') or control['assert_disclosure'] not in ('Y', 'N', '-') or control['assert_accuracy'] not in ('Y', 'N', '-') or control['assert_fraud'] not in ('Y', 'N', '-'):
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la pestaña de controles no ha establecido valor para alguna celda obligatoria en la fila %s')% (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                if control['scope'] not in ('G','P', None):
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la pestaña de controles no ha establecido un valor correcto para el alcance en la fila %s')% (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                if control['plant'] in (None, '') and control['scope'] == 'P':
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la pestaña de controles no ha establecido valor para Planta en la fila %s') % (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                if control['scope'] != 'P' and control['plant'] not in (None, ''):
                    self.errors_found += 1
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (_('En la pestaña de controles ha establecido valor para la Planta de Producción en la fila %s, mientras que la sociedad seleccionada no es Planta') % (i)),
                    )
                    return super(GaImportView, self).form_invalid(form)

                control_to_create.append(control)

        # Riesgos Compañías
        risk_sheet = wb['Company Risks']
        risk_company_to_create = []
        rows = [row for row in risk_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                risk_company = {}

                risk_company['risk_ref'] = row[0].value.strip() if row[0].value else row[0].value
                risk_company['company_ref'] = row[1].value.strip() if row[1].value else row[1].value
                risk_company['name'] = row[2].value
                risk_company['description'] = row[3].value
                risk_company['krm_activity_affected'] = row[4].value
                risk_company['krm_main_events'] = row[5].value
                risk_company['krm_exposed_staff'] = row[6].value
                risk_company['krm_main_elements'] = row[7].value
                risk_company['expert'] = [row[8].value] if row[8].value else []
                risk_company['evaluator'] = [row[9].value] if row[9].value else []

                #comprobaciones correspondientes a las referencias de los maestros asociados:
                if self.checkMandatory(_("riesgos de compañía"), risk_company, i, "risk_ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkMandatory(_("riesgos de compañía"), risk_company, i, "company_ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkCompanyObjects(_("riesgos de compañía"), risk_company, risk_to_create):
                    return super(GaImportView, self).form_invalid(form)

                #comprobaciones correspondientes a los evaluadores/expertos:
                if risk_company['expert'] not in (None, ''):
                    if self.check_user_in_company(risk_company, 'expert'):
                        return super(GaImportView, self).form_invalid(form)
                if risk_company['evaluator'] not in (None, ''):
                    if self.check_user_in_company(risk_company, 'evaluator'):
                        return super(GaImportView, self).form_invalid(form)

                risk_company_to_create.append(risk_company)

        # Control-Compañías
        control_company_sheet = wb['Company Controls']
        control_company_to_create = []
        rows = [row for row in control_company_sheet.iter_rows() if any(cell.value and str(cell.value).strip()!= '' for cell in row)]

        for row in rows:
            i= row[0].row
            if not i == 1:
                control_company = {}

                control_company['control_ref'] = row[0].value.strip() if row[0].value else row[0].value
                control_company['company_ref'] = row[1].value.strip() if row[1].value else row[1].value

                if row[2].value:
                    control_company['control_owners'] = [x for x in row[2].value.strip().replace(' ', '').split(',') if '@' in x]
                else:
                    control_company['control_owners'] = []

                if row[3].value:
                    control_company['control_supervisors'] = [x for x in row[3].value.strip().replace(' ', '').split(',') if '@' in x]
                else:
                    control_company['control_supervisors'] = []

                #comprobaciones correspondientes a las referencias a los maestros asociados:
                if self.checkMandatory(_("controles de compañía"), control_company, i, "control_ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkMandatory(_("controles de compañía"), control_company, i, "company_ref"):
                    return super(GaImportView, self).form_invalid(form)
                if self.checkCompanyObjects(_("controles de compañía"), control_company, control_to_create):
                    return super(GaImportView, self).form_invalid(form)

                #comprobaciones de los usuarios owners/supervisors
                if control_company['control_owners'] not in (None, ''):
                    if self.check_user_in_company(control_company,'control_owners'):
                        return super(GaImportView, self).form_invalid(form)
                if control_company['control_supervisors'] not in (None, ''):
                    if self.check_user_in_company(control_company,'control_supervisors'):
                        return super(GaImportView, self).form_invalid(form)

                control_company_to_create.append(control_company)

        # Vamos a crear cosas
        if self.errors_found == 0:
            dr_created, n = 0, len(domain_risk_to_create)
            for i, dr in enumerate(domain_risk_to_create):
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

            rm_created= 0
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

            r_created, n = 0, len(risk_to_create)
            for i, r in enumerate(risk_to_create):
                Risk.objects.create(
                    ref=r['ref'],
                    name=r['name'],
                    description=r['description'],
                    risk_master=RiskMaster.objects.get(ref=r['risk_master_ref']),
                    impact_inherent=r['impact_inherent'],
                    probability_inherent=r['probability_inherent'],
                    impact_residual=r['impact_residual'],
                    probability_residual=r['probability_residual'],
                    event_speed= r['event_speed'],
                    krm_activity_affected=r['krm_activity_affected'],
                    krm_main_events=r['krm_main_events'],
                    krm_exposed_staff=r['krm_exposed_staff'],
                    krm_main_elements=r['krm_main_elements'],
                )
                r_created += 1

            p_created, n = 0, len(process_to_create)
            for i,p in enumerate(process_to_create):
                Process.objects.create(
                ref=p['ref'],
                name=p['name'],
                description=p['description'],
                )
                p_created += 1

            if p_created > 0:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    (
                        _(
                            "{0} Procesos creados"
                        ).format(
                            p_created,
                        )
                    ),
                )

            s_created, n = 0, len(subprocess_to_create)
            for i,s in enumerate(subprocess_to_create):
                SubProcess.objects.create(
                    ref=s['ref'],
                    name=s['name'],
                    description=s['description'],
                    process=Process.objects.get(ref=s['process_master_ref'])
                )
                s_created += 1

            if s_created > 0:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    (
                        _(
                            "{0} Subprocesos creados"
                        ).format(
                            s_created,
                        )
                    ),
                )

            c_created, n = 0, len(control_to_create)
            for i, r in enumerate(control_to_create):
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
                    plant=r['plant'],
                    control_frequency=r['control_frequency'],
                    is_gap=r['is_gap'],
                    assert_existence=r['assert_existence'],
                    assert_completeness=r['assert_completeness'],
                    assert_valuation=r['assert_valuation'],
                    assert_rights=r['assert_rights'],
                    assert_disclosure=r['assert_disclosure'],
                    assert_accurancy=r['assert_accuracy'],
                    assert_froud=r['assert_fraud'],
                    is_elc = is_elc,
                    evidence = r['evidence'],
                    scope = r['scope']
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

            #control company
            control_company_updated = 0

            for cc in control_company_to_create:
                cont_comp = CompanyControls.objects.get(company = Company.objects.get(ref=cc['company_ref']), control = Control.objects.get(ref=cc['control_ref']))
                cont_comp.active = True
                control_company_updated += 1

                cont_comp.control_test_owners.clear() #limpiamos los campos ManyToManyField de usuarios responsables y administradores
                cont_comp.control_test_supervisors.clear()
                if cc['control_owners']:
                    for owner in cc['control_owners']:
                        cont_comp.control_test_owners.add(User.objects.get(email=owner))

                if cc['control_supervisors']:
                    for supervisor in cc['control_supervisors']:
                        cont_comp.control_test_supervisors.add(User.objects.get(email=supervisor))

                cont_comp.save()


            if control_company_updated > 0:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    (
                        _(
                            "{0} Controles asociados a compañías activados y actualizados"
                        ).format(
                            control_company_updated,
                        )
                    ),
                )

            # RiskCompany
            risk_company_updated= 0
            for rc in risk_company_to_create:
                rc_object = RiskCompany.objects.get(
                    company__ref=rc['company_ref'],
                    risk__ref=rc['risk_ref']
                )
                rc_object.active = True

                if rc['name']:
                    rc_object.name = rc['name']
                if rc['description']:
                    rc_object.description = rc['description']
                if rc['krm_activity_affected']:
                    rc_object.krm_activity_affected = rc['krm_activity_affected']
                if rc['krm_main_events']:
                    rc_object.krm_main_events = rc['krm_main_events']
                if rc['krm_exposed_staff']:
                    rc_object.krm_exposed_staff = rc['krm_exposed_staff']
                if rc['krm_main_elements']:
                    rc_object.krm_main_elements = rc['krm_main_elements']
                if rc['expert']:
                    rc_object.expert = User.objects.get(email=rc['expert'][0])
                if rc['evaluator']:
                    rc_object.evaluator = User.objects.get(email=rc['evaluator'][0])

                rc_object.save()
                risk_company_updated += 1

            if risk_company_updated > 0:
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    (
                        _(
                            "{0} Riesgos asociados a compañías activados y actualizados"
                        ).format(
                            risk_company_updated,
                        )
                    ),
                )

        return super(GaImportView, self).form_valid(form)

    def get_success_url(self):

        return reverse_lazy("configuration:ga_import")
