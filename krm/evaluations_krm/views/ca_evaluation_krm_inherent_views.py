# from django.shortcuts import render
# from django.conf import settings

# # Create your views here.
# from django.shortcuts import render
# from django.views.generic import (
#     FormView,
#     TemplateView,
#     ListView,
#     CreateView,
#     DetailView,
#     UpdateView,
#     DeleteView,
#     View
# )
# from django.contrib import messages
# from django.shortcuts import HttpResponseRedirect
# from django.urls import reverse_lazy, reverse
# from django.utils.translation import gettext as _

# from django.shortcuts import get_object_or_404
# from django.http import HttpResponse

# from django.utils.decorators import method_decorator
# from django.contrib.auth.decorators import login_required
# from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationActionForm, EvaluationTemplateAssignDownload
# from krm.evaluations.models import ControlTest

# from krm.metronic.__init__ import KTLayout
# from krm.metronic.libs.theme import KTTheme

# from krm.evaluations.forms import EvaluationCreateForm, EvaluationUpdateForm
# # from krm.evaluations.forms import EvaluationTestTemplateAssignDownload

# from krm.evaluations.models import Evaluation
# from krm.companies.models import Company
# from krm.controls.models import Control

# from krm.evaluations.forms import (
#     EvaluationActionForm,
#     EvaluationTemplateAssignDownload,
#     EvaluationDownload,
#     EvaluationAssignImportForm
# )

# from krm.users.models import User

# from krm.users.decorators import (
#     is_company_admin,
#     user_can_view_evaluation
# )

# from krm.utils.utils import clean_html


# @method_decorator([login_required, is_company_admin], name='dispatch')
# class CaEvaluationListView(ListView):
#     model = Evaluation
#     template_name = 'evaluations/CaEvaluationList.html'
#     context_object_name = 'evaluations'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)

#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Evaluaciones'), 'url': reverse(
#                 'evaluations:ca_evaluation_list')},
#         ]
#         context['page_title'] = _('Evaluaciones')
#         context['breadcrums'] = breadcrums
#         context['actions'] = [
#             {
#                 'title': _('Nuevo'),
#                 'url': reverse('evaluations:ca_evaluation_create'),
#                 'primary': True,
#                 'icon': '<i class="bi bi-plus-lg"></i>'
#             },
#         ]
#         context['js_template'] = ['js/custom/datatables.js']
#         return context

#     def get_queryset(self):
#         return Evaluation.objects.filter(company__in=self.request.user.companies_admin.all())


# @method_decorator([login_required, user_can_view_evaluation, ], name='dispatch')
# class CaEvaluationDetailView(FormView):
#     template_name = 'evaluations/CaEvaluationDetail.html'
#     form_class = EvaluationActionForm

#     def dispatch(self, request, *args, **kwargs):
#         evaluation = get_object_or_404(Evaluation, pk=self.kwargs.get("pk"))
#         self.evaluation = evaluation
#         return super().dispatch(request, *args, **kwargs)

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)
#         context['evaluation'] = self.evaluation
#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Evaluaciones'), 'url': reverse(
#                 'evaluations:ca_evaluation_list')},
#             {'title': self.evaluation.ref}
#         ]
#         context['page_title'] = f"{_('Evaluación')} : {self.evaluation.ref}"
#         context['breadcrums'] = breadcrums
#         context['actions'] = [
#             {
#                 'title': _('Editar'),
#                 'url': reverse('evaluations:ca_evaluation_update', kwargs={'pk': self.evaluation.pk}),
#                 'primary': True,
#                 'icon': '<i class="bi bi-pencil"></i>'
#             },
#         ]
#         context['js_template'] = ['js/custom/datatables.js']

#         return context

#     def form_valid(self, form):
#         action = form.cleaned_data["action"]
#         evaluation = self.evaluation

#         if action == "i":
#             evaluation.status = "EP"
#             evaluation.save()
#             users_notificated = []
#             for ct in evaluation.control_tests.all():
#                 ct.status = "WO"
#                 ct.save()
#                 if ct.control_test_owner not in users_notificated:
#                     users_notificated.append(ct.control_test_owner)
#                     ct.send_notification()

#             messages.add_message(
#                 self.request,
#                 messages.SUCCESS,
#                 _("Evaluación iniciada correctamente"),
#             )
#         elif action == 'f':
#             evaluation.status = "FI"
#             evaluation.save()
#             evaluation.control_tests.update(
#                 status='FI'
#             )

#             messages.add_message(
#                 self.request,
#                 messages.SUCCESS,
#                 _("Evaluación finalizada correctamente"),
#             )
#         # elif action == 'd':

#         #     wb.save(response)

#         #     return response

#         # elif action == 'a':
#         #     filename = "{} template_asign_evaluation.xls".format(evaluation.pk)
#         #     response = HttpResponse(content_type="application/ms-excel")
#         #     response["Content-Disposition"] = 'attachment; filename="{}"'.format(
#         #         filename
#         #     )

#         #     wb = xlwt.Workbook(encoding="utf-8")
#         #     ws = wb.add_sheet("Controls")

#         #     ws.col(0).width = 256 * 25
#         #     ws.col(1).width = 256 * 25
#         #     ws.col(2).width = 256 * 40
#         #     ws.col(3).width = 256 * 40
#         #     ws.col(4).width = 256 * 40
#         #     ws.col(4).width = 256 * 40

#         #     # Sheet header, first row
#         #     row_num = 0

#         #     font_style = xlwt.XFStyle()
#         #     font_style.font.bold = True

#         #     columns = [
#         #         "PK",
#         #         "REF",
#         #         "CONTROL SUPERVISOR",
#         #         "CONTROL OWNER",
#         #         "CONTROL - REF",
#         #         "CONTROL",
#         #     ]

#         #     for col_num in range(len(columns)):
#         #         ws.write(row_num, col_num, columns[col_num], font_style)

#         #     # Sheet body, remaining rows
#         #     font_style = xlwt.XFStyle()

#         #     for ct in evaluation.control_tests.all().order_by("control__ref"):
#         #         row_num += 1
#         #         ws.write(row_num, 0, ct.pk, font_style)
#         #         ws.write(row_num, 1, ct.identifier, font_style)
#         #         if ct.control_test_supervisor is not None:
#         #             ws.write(
#         #                 row_num, 2, ct.control_test_supervisor.email, font_style)
#         #         if ct.control_test_owner is not None:
#         #             ws.write(row_num, 3, ct.control_test_owner.email, font_style)
#         #         ws.write(row_num, 4, ct.control.ref, font_style)
#         #         ws.write(row_num, 5, clean_html(ct.control.name), font_style)

#         #     # Ocultamos la columna de los pk
#         #     ws.col(0).hidden = 1

#         #     wb.save(response)

#         #     return response

#         return super().form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy(
#             "evaluations:ca_evaluation_detail",
#             kwargs={"pk": self.evaluation.pk},
#         )


# @method_decorator([login_required, is_company_admin, ], name='dispatch')
# class CaEvaluationCreateView(FormView):
#     form_class = EvaluationCreateForm
#     model = Evaluation
#     template_name = 'evaluations/CaEvaluationCreate.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)

#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Evaluaciones'), 'url': reverse(
#                 'evaluations:ca_evaluation_list')},
#             {'title': _('Nuevo'), 'url': reverse(
#                 'evaluations:ca_evaluation_create')},
#         ]
#         context['page_title'] = _('Nueva Evaluación')
#         context['breadcrums'] = breadcrums

#         return context

#     def get_success_url(self):

#         return reverse_lazy(
#             'evaluations:ca_evaluation_list'
#         )

#     def form_valid(self, form):
#         controls_created = 0
#         evaluations_created = 0

#         companies = Company.objects.filter(
#             pk__in=(form.cleaned_data["companies"]))
#         controls = Control.objects.filter(
#             pk__in=(form.cleaned_data["controls"]))

#         for company in companies:
#             evaluation = Evaluation.objects.create(
#                 ref=f'{form.cleaned_data["ref"]} - {company.name}',
#                 company=company,
#                 description=form.cleaned_data["description"],
#                 date_begin=form.cleaned_data["date_begin"],
#                 date_intermediate=form.cleaned_data["date_intermediate"],
#                 date_end=form.cleaned_data["date_end"],
#                 certification_year=form.cleaned_data["certification_year"],
#                 certification_period=form.cleaned_data["certification_period"],
#                 allow_self_autosupervision=form.cleaned_data[
#                     "allow_self_autosupervision"
#                 ],
#             )

#             # Para cada evaluación hay que crear los test controls de los controles que se han pasado
#             for control in controls:
#                 control_test = ControlTest.objects.create(
#                     evaluation=evaluation,
#                     control=control,
#                     date_begin=form.cleaned_data["date_begin"]
#                 )

#                 controls_created += 1

#             evaluations_created += 1

#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             _("%s Evaluaciones creadas correctamente") % str(evaluations_created),
#         )

#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             _("%s Test de Control creados correctamente") % str(controls_created),
#         )
#         return super().form_valid(form)


# @method_decorator([login_required, is_company_admin, ], name='dispatch')
# class CaEvaluationUpdateView(UpdateView):
#     form_class = EvaluationUpdateForm
#     model = Evaluation
#     template_name = 'evaluations/CaEvaluationUpdate.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)

#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Evaluaciones'), 'url': reverse(
#                 'evaluations:ca_evaluation_list')},
#             {'title': _('Editar')},
#         ]
#         context['page_title'] = _('Editar Evaluación')
#         context['breadcrums'] = breadcrums

#         return context

#     def get_success_url(self):

#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             _('Evaluación actualizada correctamente')
#         )
#         return reverse_lazy(
#             'evaluations:ca_evaluation_detail',
#             kwargs={"pk": self.object.pk},
#         )


# @method_decorator([login_required, is_company_admin, ], name='dispatch')
# class CaEvaluationDeleteView(DeleteView):
#     model = Evaluation
#     template_name = "_includes/_base_confirm_delete.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)

#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Evaluaciones'), 'url': reverse(
#                 'evaluations:ca_evaluation_list')},
#             {'title': _('Eliminar')},
#         ]
#         context['page_title'] = _(
#             "Eliminar Evaluación: #%s") % str(self.object.ref)
#         context['breadcrums'] = breadcrums

#         return context

#     def get_success_url(self):
#         messages.add_message(
#             self.request, messages.SUCCESS, _(
#                 "Evaluación eliminada correctamente")
#         )
#         return reverse_lazy("evaluations:ca_evaluation_list")

#     def get_confirm_text_message(self):
#         return _(
#             '<span class="kt-font-bold">¿Seguro que desea eliminar la Evaluación y los datos asociados?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los riesgos y controles asociados al mismo.</span>'
#         ).format(str(self.object.ref))


# @method_decorator((login_required, user_can_view_evaluation), name="dispatch")
# class CaEvaluationAssignImport(FormView):
#     template_name = "evaluations/GaEvaluationImportAssign.html"
#     form_class = EvaluationAssignImportForm

#     def dispatch(self, request, *args, **kwargs):
#         self.evaluation = get_object_or_404(
#             Evaluation, pk=self.kwargs.get("pk"))
#         return super(CaEvaluationAssignImport, self).dispatch(
#             request, request, *args, **kwargs
#         )

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)
#         context['evaluation'] = self.evaluation
#         context['page_title'] = f"{_('Asignar controles para la evaluación')} : {self.evaluation.ref}"
#         return context

#     def form_valid(self, form):
#         input_excel = self.request.FILES["evaluation_assign_file"]
#         book = open_workbook(file_contents=input_excel.read())

#         control_test_sheet = book.sheet_by_index(0)
#         control_tests = []
#         # Primero tenemos que controlar que todos los controles existen y pertenecen al Test de Proceso
#         for row in range(control_test_sheet.nrows):
#             if row > 0:
#                 control_test_pk = int(control_test_sheet.cell(row, 0).value)
#                 control_test_supervisor_email = str(
#                     control_test_sheet.cell(row, 2).value
#                 )
#                 control_test_owner_email = str(
#                     control_test_sheet.cell(row, 3).value)
#                 # Comprobamos que el test de control existe y que pertenece al test de proceso
#                 control_test = get_object_or_404(
#                     ControlTest, pk=control_test_pk)
#                 if control_test.evaluation != self.evaluation:
#                     messages.add_message(
#                         self.request,
#                         messages.ERROR,
#                         (
#                             _(
#                                 "En la fila %s hay un control que no pertenece a dicho Test de Control. Se ha abortado la importación"
#                             )
#                             % str(row + 1)
#                         ),
#                     )
#                     return super(CaEvaluationAssignImport, self).form_invalid(form)
#                     break
#                 # Cromprobamos que el control owner existe y que pertenecen a la compañía del Test de Proceso
#                 if control_test_owner_email != "":
#                     try:
#                         control_test_owner = User.objects.get(
#                             email=control_test_owner_email
#                         )
#                     except Exception as e:
#                         messages.add_message(
#                             self.request,
#                             messages.ERROR,
#                             (
#                                 _("En la fila %s el control owner no existe")
#                                 % str(row + 1)
#                             ),
#                         )
#                         return super(CaEvaluationAssignImport, self).form_invalid(form)
#                     control_tests.append(control_test)
#                     if not control_test_owner.companies.filter(
#                         pk=self.evaluation.company.pk
#                     ):
#                         messages.add_message(
#                             self.request,
#                             messages.ERROR,
#                             (
#                                 _(
#                                     "En la fila %s el control owner no pertenece a la compañía sobre la que está realizado la evaluación"
#                                 )
#                                 % str(row + 1)
#                             ),
#                         )
#                         return super(CaEvaluationAssignImport, self).form_invalid(form)
#                     control_test.control_test_owner = control_test_owner
#                 else:
#                     control_test.control_test_owner = None

#                 if control_test_supervisor_email != "":
#                     #  Comprobamos que el control supervisor existe y que pertenecen a la compañía del Test de Proceso
#                     try:
#                         control_test_supervisor = User.objects.get(
#                             email=control_test_supervisor_email
#                         )
#                     except Exception as e:
#                         messages.add_message(
#                             self.request,
#                             messages.ERROR,
#                             (
#                                 _("En la fila %s el control owner no existe")
#                                 % str(row + 1)
#                             ),
#                         )
#                         return super(CaEvaluationAssignImport, self).form_invalid(form)
#                     control_tests.append(control_test)
#                     if not control_test_supervisor.companies.filter(
#                         pk=self.evaluation.company.pk
#                     ):
#                         messages.add_message(
#                             self.request,
#                             messages.ERROR,
#                             (
#                                 _(
#                                     "En la fila %s el control owner no pertenece a la compañía sobre la que está realizado la evaluación"
#                                 )
#                                 % str(row + 1)
#                             ),
#                         )
#                         return super(CaEvaluationAssignImport, self).form_invalid(form)
#                     control_test.control_test_supervisor = control_test_supervisor
#                 else:
#                     control_test.control_test_supervisor = None

#                 if (
#                     control_test.control_test_owner is not None
#                     and control_test.control_test_owner
#                     == control_test.control_test_supervisor
#                     and control_test.evaluation.allow_self_autosupervision is False
#                 ):
#                     messages.add_message(
#                         self.request,
#                         messages.ERROR,
#                         (
#                             _(
#                                 "En la fila %s el control owner y el control supervisor son el mismo usuario. La evaluación no permite la autosupervisión"
#                             )
#                             % str(row + 1)
#                         ),
#                     )
#                     return super(CaEvaluationAssignImport, self).form_invalid(form)

#                 control_tests.append(control_test)

#         for control_test in control_tests:
#             control_test.save()

#         messages.add_message(
#             self.request, messages.SUCCESS, (_(
#                 "Controles asignados correctamente"))
#         )

#         return super(CaEvaluationAssignImport, self).form_valid(form)

#     def get_success_url(self):
#         return reverse_lazy(
#             "evaluations:ca_evaluation_detail", kwargs={"pk": self.evaluation.pk}
#         )
