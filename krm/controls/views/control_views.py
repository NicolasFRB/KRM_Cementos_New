from django.shortcuts import render
import xlwt
import re

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
from django.http import HttpResponse

from django.utils.decorators import method_decorator

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.controls.forms import ControlCreateForm
from krm.controls.models import Control
from krm.risks.models import Risk
from krm.process.models import SubProcess
from krm.companies.models import Company, CompanyControls

from krm.users.decorators import is_global_admin

from krm.controls.forms import (
    ControlImportForm,
    DownloadControlsActionForm
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlListView(ListView,FormView):
    model = Control
    template_name = 'controls/GaControlList.html'
    form_class = DownloadControlsActionForm
    context_object_name = 'controls'
    queryset = Control.objects.all().prefetch_related(
        'sub_processes').prefetch_related('risks__risk_master__domain_risk')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
        ]
        context['page_title'] = _('Controles')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('controls:ga_control_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def form_valid(self, form):
        action = form.cleaned_data["action"]

        if action == 'd':

            # Comienzo de la creacion de archivo de descarga del Test de Proceso
            filename = "control_company.xls"
            response = HttpResponse(content_type="application/ms-excel")
            response["Content-Disposition"] = 'attachment; filename="{}"'.format(
                filename
            )

            wb = xlwt.Workbook(encoding="utf-8")

            # Sheet header, first row
            row_num = 0

            font_style_title = xlwt.easyxf("align: vert centre, horiz left")
            font_style_title.font.bold = True

            font_style_title_wrap = xlwt.easyxf(
                "align: vert centre, horiz left, wrap yes"
            )
            font_style_title_wrap.font.bold = True

            font_style_body = xlwt.easyxf("align: vert top, horiz left")
            font_style_body_wrap = xlwt.easyxf(
                "align: vert top, horiz left, wrap yes"
            )

            for company in Company.objects.all():
                row_num = 0
                ws = wb.add_sheet("{}".format(company.ref))

                ws.col(0).width = 256 * 30
                ws.col(1).width = 256 * 25
                ws.col(2).width = 256 * 50
                ws.col(3).width = 256 * 80
                ws.col(4).width = 256 * 80
                ws.col(5).width = 256 * 80
                ws.col(6).width = 256 * 80

                columns = [
                    "COMPAÑIA",  # 0
                    "CONTROL REF",  # 1
                    "NOMBRE",  # 2
                    "DESCRIPCIÓN",  # 3
                    "RIESGOS",  # 4
                    "SUB PROCESOS",  # 5
                    "KEY CONTROL",  # 6
                    "TIPO",  # 7
                    "AUTOMATICO",  # 8
                    "FRECUENCIA",  # 9
                    "CONTROL OWNER",  # 10
                    "CONTROL SUPERVISOR",  # 11
                    "ALCANCE",  # 12
                    ]

                for col_num in range(len(columns)):
                    if col_num in (21, 28):
                        ws.write(
                            row_num, col_num, columns[col_num], font_style_title_wrap
                        )
                    else:
                        ws.write(row_num, col_num,
                                columns[col_num], font_style_title)

                if CompanyControls.objects.filter(company = company,active = True).count() > 0:
                    for comp_cont in CompanyControls.objects.filter(company = company,active = True):
                        row_num += 1
                        ws.write(
                            row_num, 0, comp_cont.company.name, font_style_body
                        )  # 0
                        ws.write(
                            row_num, 1, comp_cont.control.ref, font_style_body
                        )  # 1
                        ws.write(
                            row_num, 2, comp_cont.control.name, font_style_body
                        )  # 2
                        ws.write(
                            row_num, 3, comp_cont.control.description, font_style_body
                        )  # 3

                        risks = []
                        if comp_cont.control.risks.count() > 0:
                            for risk in comp_cont.control.risks.all():
                                risks.append(risk.ref)
                            all_risks = ','.join(risks)
                            ws.write(
                                row_num, 4, all_risks, font_style_body
                            )  # 4

                        sub_processes = []   
                        if comp_cont.control.sub_processes.count() > 0:
                            for sp in comp_cont.control.sub_processes.all():
                                sub_processes.append(sp.name)
                            all_sp = ','.join(sub_processes)
                            ws.write(
                                row_num, 5, all_sp, font_style_body
                            )  # 5
                        ws.write(
                            row_num, 6, comp_cont.control.key_control, font_style_body
                        )  # 6
                        ws.write(
                            row_num, 7, comp_cont.control.get_control_type_display(), font_style_body
                        )  # 7
                        ws.write(
                            row_num, 8, comp_cont.control.get_automation_display(), font_style_body
                        )  # 8
                        ws.write(
                            row_num, 9, comp_cont.control.get_control_frequency_display(), font_style_body
                        )  # 9
                        
                        owners = []   
                        if comp_cont.control_test_owners.count() > 0:
                            for co in comp_cont.control_test_owners.all():
                                owners.append(co.email)
                            all_co = ','.join(owners)
                            ws.write(
                                row_num, 10, all_co, font_style_body
                            )  # 10
                        supervisors = []   
                        if comp_cont.control_test_supervisors.count() > 0:
                            for cs in comp_cont.control_test_supervisors.all():
                                supervisors.append(cs.email)
                            all_cs = ','.join(supervisors)
                            ws.write(
                                row_num, 11, all_cs, font_style_body
                            )  # 11

                        ws.write(
                            row_num, 12, comp_cont.control.get_scope_display(), font_style_body
                        )  # 12
                    
            wb.save(response)
            return response

        return super().form_valid(form)


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlDetailView(DetailView):
    model = Control
    template_name = 'controls/GaControlDetail.html'
    context_object_name = 'control'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Control')} : {self.object.ref}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('controls:ga_control_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]

        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlCreateView(CreateView):
    form_class = ControlCreateForm
    model = Control
    template_name = 'controls/GaControlCreate.html'

    def get_initial(self):
        if 'domain_Control' in self.kwargs:
            risk = get_object_or_404(
                Risk, pk=self.kwargs.get('risk')
            )
            return {
                'risk': risk
            }
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': _('Nuevo control'), 'url': reverse(
                'controls:ga_control_create')},
        ]
        context['page_title'] = _('Nuevo Control')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Control creado correctamente')
        )
        return reverse_lazy(
            'controls:ga_control_list'
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlUpdateView(UpdateView):
    form_class = ControlCreateForm
    model = Control
    template_name = 'controls/GaControlUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Control')
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Control actualizado correctamente')
        )
        return reverse_lazy(
            'controls:ga_control_detail',
            kwargs={"pk": self.object.pk},
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlDeleteView(DeleteView):
    model = Control
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Riesgo")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Control eliminado correctamente")
        )
        return reverse_lazy("controls:ga_control_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el Control: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object))


@method_decorator([is_global_admin, ], name='dispatch')
class GaControlImport(FormView):
    template_name = "process/ga/GaControlImport.html"
    form_class = ControlImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Controles'), 'url': reverse(
                'controls:ga_control_list')},
        ]
        context['page_title'] = _('Controles')
        context['breadcrums'] = breadcrums

        return context

    def form_valid(self, form):
        input_excel = self.request.FILES["controls_file"]
        book = open_workbook(file_contents=input_excel.read())

        # Controles
        control_sheet = book.sheet_by_index(0)
        control_ref_list = []
        for row in range(control_sheet.nrows):
            if row > 0:
                # Los riesgos hay que validarlos y ver que existen y que no hay nada raro
                risks_ref = str(int(control_sheet.cell(row, 0).value))
                risks_ref.strip()
                risks_ref = risks_ref.split(',')
                for r in risks_ref:
                    if not isinstance(r, int):
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(u'En la fila %s "Riesgo - ID" no no es válido')
                                % str(row + 1)
                            ),
                        )
                        return super(GaControlImport, self).form_invalid(form)
                    if Risk.objects.filter(pk=r).count() == 0:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(u'En la fila %s hay un "Riesgo - ID" que no existe')
                                % (str(row + 1), r)
                            ),
                        )
                        return super(GaControlImport, self).form_invalid(form)

                # Subprocesos
                subprocess_ref = str(int(control_sheet.cell(row, 0).value))
                subprocess_ref = subprocess_ref.split(',')
                for r in subprocess_ref:
                    if not isinstance(r, int):
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(u'En la fila %s "Subproceso - ID" no no es válido')
                                % str(row + 1)
                            ),
                        )
                        return super(GaControlImport, self).form_invalid(form)
                    if SubProcess.objects.filter(pk=r).count() == 0:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(u'En la fila %s hay un "Riesgo - ID" que no existe')
                                % (str(row + 1), r)
                            ),
                        )
                        return super(GaControlImport, self).form_invalid(form)

                control_ref = str(control_sheet.cell(row, 1).value)
                if type(control_sheet.cell(row, 1).value) == float:
                    control_ref = str(int(control_sheet.cell(row, 1).value))
                else:
                    control_ref = str(control_sheet.cell(row, 1).value)
                control_ref_list.append(control_ref)
                if len(control_ref) > 140 or control_ref == "":
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - ID" no puede ser vacío ni tener una extensión mayor de 140 caracteres'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_objetive = str(control_sheet.cell(row, 2).value).replace(
                    "\n", "<br>"
                )
                if len(control_objetive) > 10000:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - Objetivo" no puede tener una extensión mayor de 10000 caracteres'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_description = str(control_sheet.cell(row, 3).value).replace(
                    "\n", "<br>"
                )
                if len(control_description) > 10000:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - Descripción" no puede tener una extensión mayor de 10000 caracteres'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_action_plan = str(control_sheet.cell(row, 4).value).replace(
                    "\n", "<br>"
                )
                if len(control_action_plan) > 10000:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - Plan de acción" no puede tener una extensión mayor de 10000 caracteres'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_testing_procedure = str(
                    control_sheet.cell(row, 5).value
                ).replace("\n", "<br>")
                if len(control_testing_procedure) > 10000:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - Procedimiento de testeo" no puede tener una extensión mayor de 10000 caracteres'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_key_control = str(control_sheet.cell(row, 6).value)
                if control_key_control not in ("", "X"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "KEY CONTROL (X)" solo admite valores vacíos o X'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_control_type = str(control_sheet.cell(row, 7).value)
                if control_control_type not in ("P", "D"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - Tipo" solo admite los valores P y D'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_automation = str(control_sheet.cell(row, 8).value)
                if control_automation not in ("A", "M", "S"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - AUTOMATIZACIÓN" solo admite los valores A, M Y S'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_systems = str(control_sheet.cell(row, 9).value).replace(
                    "\n", "<br>"
                )
                if len(control_systems) > 140:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - Sistemas" no puede tener una extensión mayor de 140 caracteres'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_control_frequency = str(
                    control_sheet.cell(row, 10).value)
                if control_control_frequency not in (
                    "CO",
                    "BD",
                    "DI",
                    "1W",
                    "2W",
                    "1M",
                    "2M",
                    "3T",
                    "6M",
                    "1Y",
                    "2Y",
                    "3Y"
                ):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - Periodicidad" solo admite los valores CO, BD, DI, 1W, 2W, 1M, 2M, 3T, 6M, 1Y, 2Y, 3Y'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_is_gap = str(control_sheet.cell(row, 11).value)
                if control_is_gap not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control GAP" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_assert_existence = str(
                    control_sheet.cell(row, 12).value)
                if control_assert_existence not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control Existency" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_assert_completeness = str(
                    control_sheet.cell(row, 13).value)
                if control_assert_completeness not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control Completness" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_assert_valuation = str(
                    control_sheet.cell(row, 14).value)
                if control_assert_valuation not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control Valuation" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_assert_rights = str(control_sheet.cell(row, 15).value)
                if control_assert_rights not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control Obligation Right" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_assert_disclosure = str(
                    control_sheet.cell(row, 16).value)
                if control_assert_disclosure not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control Presentation" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_assert_accurancy = str(
                    control_sheet.cell(row, 17).value)
                if control_assert_accurancy not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control Accurancy" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                control_assert_froud = str(control_sheet.cell(row, 18).value)
                if control_assert_froud not in ("-", "Y", "N"):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control Fraud" solo admite los valores -, Y y N'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

                # Cogemos el valor y quitamos los espacios
                control_regulatory_framework = str(
                    control_sheet.cell(row, 19).value
                ).replace(" ", "")
                control_regulatory_framework_list = control_regulatory_framework.split(
                    ","
                )
                for rf in control_regulatory_framework_list:
                    if RegulatoryFramework.objects.filter(acronym=rf).count() == 0:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _(u'En la fila %s "Control Marco Normativo " no válido')
                                % str(row + 1)
                            ),
                        )
                        return super(ProcessImport, self).form_invalid(form)
                # control_regulatory_frameworks = RegulatoryFramework.objects.filter(acronym_in=control_regulatory_framework_list)

                # if control_regulatory_framework not in ('SCIIF', 'MPD', 'AML', 'CFT', 'KYC', 'FI',):
                #     messages.add_message(
                #         self.request,
                #         messages.ERROR,
                #         (
                #             _(u'En la fila %s "Control Marco Normativo " solo admite los valores SCIIF, MPD, AML, CFT, KYC, FI') % str(row+1)
                #         )
                #     )
                #     return super(
                #         ProcessImport,
                #         self
                #     ).form_invalid(form)

                if len(control_ref_list) != len(set(control_ref_list)):
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _(
                                u'En la fila %s "Control - ID" está repetido. Los identificadores de los controles deben ser únicos por proceso'
                            )
                            % str(row + 1)
                        ),
                    )
                    return super(ProcessImport, self).form_invalid(form)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            (
                _(
                    "Proceso importado correctamente con {0} subprocesos, {1} riesgos y {2} controles"
                ).format(
                    str(len(subprocess_to_create)),
                    str(len(risks_news)),
                    str(len(controls_news)),
                )
            ),
        )

        return super(ProcessImport, self).form_valid(form)

    def get_success_url(self):

        return reverse_lazy("process:ga_process_detail", kwargs={"pk": self.process_pk})
