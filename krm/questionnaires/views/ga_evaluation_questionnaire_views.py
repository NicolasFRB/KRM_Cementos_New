import json
import uuid
import re
import xlsxwriter
from openpyxl import load_workbook
from io import BytesIO

from django.http import HttpResponse

from django.views.generic import (
    FormView,
    DetailView,
    ListView
)
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from krm.metronic.__init__ import KTLayout

from krm.questionnaires.models import EvaluationQuestionnaire

from krm.questionnaires.forms import EvaluationQuestionnaireCreateForm

from krm.questionnaires.forms import (
    EvaluationQuestionnaireActionForm,
)

from krm.users.decorators import is_global_admin, user_can_view_evaluation


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationQuestionnaireListView(ListView):
    model = EvaluationQuestionnaire
    template_name = 'evaluation_questionnaires/GaEvaluationQuestionnaireList.html'
    # context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
        ]
        context['page_title'] = _('Evaluaciones de Cuestionarios')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluation_questionnaires:ga_evaluation_questionnaire_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]

        evaluations_pending = EvaluationQuestionnaire.objects.filter(
            status='EP')
        evaluations_finished = EvaluationQuestionnaire.objects.filter(
            status='FI')

        context['evaluations_pending'] = evaluations_pending
        context['evaluations_finished'] = evaluations_finished

        return context


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationQuestionnaireCreateView(FormView):
    form_class = EvaluationQuestionnaireCreateForm
    template_name = 'evaluation_questionnaires/GaEvaluationQuestionnaireCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Cuestionarios'), 'url': reverse(
                'evaluation_questionnaires:ga_evaluation_questionnaire_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluation_questionnaires:ga_evaluation_questionnaire_create')},
        ]
        context['page_title'] = _('Nueva Evaluación de Cuestionario')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def get_success_url(self):
        return reverse_lazy(
            'evaluation_questionnaires:ga_evaluation_questionnaire_list'
        )

    def form_valid(self, form):

        from krm.questionnaires.models import (
            Question,
            QuestionTest
        )
        from krm.users.models import User

        users_notificated = []
        question_test_to_notify = []

        question_test_created = 0

        questions_to_evaluate = json.loads(
            form.cleaned_data["questions_to_evaluate"])

        ref = form.cleaned_data["ref"]
        if EvaluationQuestionnaire.objects.filter(
            ref=form.cleaned_data["ref"]
        ).count() > 0:
            ref = f'{form.cleaned_data["ref"]} - {uuid.uuid4().hex}'

        evaluation = EvaluationQuestionnaire()
        evaluation.ref = ref
        evaluation.description = form.cleaned_data["description"]
        evaluation.date_begin = form.cleaned_data["date_begin"]
        evaluation.date_end = form.cleaned_data["date_end"]
        evaluation.certification_period = form.cleaned_data["certification_period"]
        evaluation.questionnaire = form.cleaned_data["questionnaire"]
        evaluation.save()

        # Para cada pregunta seleccionada, se crea un question_test
        for question in questions_to_evaluate:
            q = Question.objects.get(
                pk=question["pk"])
            for evaluator in question["evaluators"]:
                question_test = QuestionTest()
                question_test.evaluation = evaluation
                question_test.question = q
                question_test.title = q.title
                question_test.evaluator = User.objects.get(pk=evaluator)
                question_test.status = 1
                question_test.save()
                question_test_created += 1
                if question_test.evaluator not in users_notificated:
                    users_notificated.append(question_test.evaluator)
                    question_test_to_notify.append(question_test)

        from krm.questionnaires.tasks import question_test_send_notification
        for qt in question_test_to_notify:
            question_test_send_notification.delay(qt.pk)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(f'Evaluacion {ref} creada correctamente con {question_test_created} preguntas')
        )

        return super().form_valid(form)


@method_decorator([is_global_admin, ], name='dispatch')
class GaEvaluationQuestionnaireDetailView(DetailView, FormView):
    template_name = 'evaluation_questionnaires/GaEvaluationQuestionnaireDetail.html'
    model = EvaluationQuestionnaire
    context_object_name = 'evaluation'
    form_class = EvaluationQuestionnaireActionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Cuestionario'), 'url': reverse(
                'evaluation_questionnaires:ga_evaluation_questionnaire_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Evaluación de Cuestionario')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def form_valid(self, form):
        action = form.cleaned_data["action"]
        evaluation = self.get_object()

        if action == 'finish':
            evaluation.status = 'FI'
            evaluation.question_tests.update(status=2)
            evaluation.save()

            messages.add_message(
                self.request,
                messages.SUCCESS,
                _(f"Evaluación {evaluation.ref} finalizada correctamente"),
            )

        if action == 'download':
            import io

            filename = f'questionnaire_evaluation_{evaluation.ref}.xlsx'

            # Create an in-memory output file for the new workbook.
            output = io.BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})
            text_wrap = workbook.add_format({'text_wrap': True})

            columns = [
                "QUESTION",
                "EVALUATOR",
                "ANSWER",
                "STATUS",
                "DESCRIPTION",
                "DATE",
            ]

            for index, col_name in enumerate(columns):
                worksheet.write(0, index, col_name, bold)

            worksheet.set_column(0, 1, 70)  # Question
            worksheet.set_column(1, 1, 25)  # Evaluator
            worksheet.set_column(2, 1, 25)  # Answer
            worksheet.set_column(3, 1, 25)  # Status
            worksheet.set_column(4, 1, 25)  # Description
            worksheet.set_column(5, 1, 25)  # Date

            row = 1

            for question in evaluation.question_tests.all():
                worksheet.write(row, 0, question.question.title, text_wrap)
                worksheet.write(row, 1, question.evaluator.username)
                worksheet.write(row, 2, question.get_answer_display())
                worksheet.write(row, 3, question.get_status_display())
                worksheet.write(row, 4, question.description)
                worksheet.write(
                    row, 5, question.modified.strftime("%d/%m/%Y %H:%M:%S"))
                row += 1

            # Close the workbook before sending the data.
            workbook.close()

            # Rewind the buffer.
            output.seek(0)

            # Set up the Http response.
            response = HttpResponse(
                output,
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            response['Content-Disposition'] = 'attachment; filename=%s' % filename

            return response

            # columns = [
            #     "QUESTION",
            #     "EVALUATOR",
            #     "ANSWER",
            #     "STATUS",
            #     "DESCRIPTION",
            #     "DATE",
            # ]

            # for col_num in range(len(columns)):
            #     ws.write(row_num, col_num, columns[col_num], font_style)

            # # Sheet body, remaining rows
            # font_style = xlwt.XFStyle()

            # for qt in evaluation.question_tests.all().order_by("question"):
            #     row_num += 1
            #     ws.write(row_num, 0, qt.title, font_style)
            #     ws.write(row_num, 1, qt.evaluator.email, font_style)
            #     ws.write(row_num, 2, qt.get_answer_display, font_style)
            #     ws.write(row_num, 3, qt.get_status_display, font_style)
            #     ws.write(row_num, 4, qt.description, font_style)
            #     ws.write(row_num, 4, qt.modified, font_style)

            # # Ocultamos la columna de los pk
            # ws.col(0).hidden = 1

            # wb.save(response)

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "evaluation_questionnaires:ga_evaluation_questionnaire_detail",
            kwargs={'pk': self.get_object().pk}
        )
