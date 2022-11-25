from django.shortcuts import render
from django.conf import settings
import json
import uuid

import re

# Create your views here.
from django.shortcuts import render

from django.views.generic import (
    FormView,
    DetailView,
    ListView
)
from django.contrib import messages
from django.shortcuts import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext as _

from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import (
    EvaluationKrmResidual,
    RiskTestResidual,
    RiskCompanyResidual
)
from krm.companies.models import (
    CompanyDomainRiskEvaluator,
    Company
)

from krm.risks.models import RiskCompany
from krm.questionnaires.models import EvaluationQuestionnaire

from krm.questionnaires.forms import EvaluationQuestionnaireCreateForm

from krm.evaluations_krm.forms import (
    EvaluationResidualCreateForm,
    EvaluationResidualCompleteForm,
)

from krm.evaluations.forms import (
    EvaluationActionForm
)

from krm.users.decorators import is_global_admin, user_can_view_evaluation

from krm.utils.utils import clean_html


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
            {'title': _('Evaluaciones de Cuestionsrios'), 'url': reverse(
                'evaluations_krm:ga_evaluation_inherent_list')},
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
    model = EvaluationQuestionnaire
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
            Questionnaire,
            Question,
            QuestionTest
        )
        from krm.users.models import User

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

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _(f'Evaluacion creada correctamente con {question_test_created} Question Test pertenecientes')
        )

        return super().form_valid(form)


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationQuestionnaireDetailView(DetailView):
    template_name = 'evaluation_questionnaires/GaEvaluationQuestionnaireDetail.html'
    model = EvaluationQuestionnaire

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.evaluation
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Cuestionario'), 'url': reverse(
                'evaluation_questionnaires:ga_evaluation_questionnaire_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación de Cuestionario')} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums

        context['js_template'] = ['js/custom/datatables.js']

        return context


# @method_decorator([login_required, is_global_admin], name='dispatch')
# class GaEvaluationQuestionnaireAdminComplete(DetailView, FormView):
#     template_name = 'evaluation_questionnaires/GaEvaluationQuestionnaireAdminComplete.html'
#     model = EvaluationKrmResidual
#     context_object_name = 'evaluation'
#     form_class = EvaluationResidualCompleteForm

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)

#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Evaluaciones de Riesgo Residual')}
#         ]
#         context['page_title'] = f"{_('Evaluación de Riesgos Residuals')} : {self.object.ref}"
#         context['breadcrums'] = breadcrums

#         # SIMPLIFICACION
#         # uso risk_test (nomenclatura), no son risk_test, son risk_company
#         risk_tests = self.object.risk_company_residuals.all()

#         for r in risk_tests:
#             r.controls_attempt_to_mitigate = r.get_controls_attempt_to_mitigate()
#             r.test_controls_attempt_to_mitigate = r.get_test_controls_attempt_to_mitigate()

#         context['risks_test_residual'] = sorted(
#             risk_tests, key=lambda t: t.get_latest_severity_inherent, reverse=True)

#         context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

#         context['js_template'] = ['js/custom/datatables.js']

#         return context

#     def form_valid(self, form):
#         evaluation = self.get_object()
#         RiskTestResidual.objects.filter(
#             evaluation=evaluation
#         ).update(
#             status=3
#         )

#         # Ahora para los que no ha completado el administrador de la compañía, debemos completar con los valores agregados que han dado los evaluadores

#         for rr in RiskTestResidual.objects.filter(evaluation=evaluation):
#             rr.status = 3
#             # Ahora buscamos el Risk Company Residual
#             rcr = RiskCompanyResidual.objects.get(
#                 evaluation=evaluation,
#                 risk_company=rr.risk
#             )

#             if rcr.probability_level_residual_administrator == 0:
#                 if rcr.probability_level_residual_evaluator_aggregate_rounded == 0:
#                     rcr.probability_level_residual_administrator = 4
#                 else:
#                     rcr.probability_level_residual_administrator = rcr.probability_level_residual_evaluator_aggregate_rounded
#             if rcr.description_administrator == '':
#                 rcr.description_administrator = _('--Sin completar--')

#             rcr.save()
#             rr.save()

#         evaluation.status = 'FI'
#         evaluation.admin_supervisor = self.request.user
#         evaluation.save()
#         return super().form_valid(form)

#     def get_success_url(self):

#         messages.add_message(
#             self.request, messages.SUCCESS, _(
#                 "Evaluación supervisada correctamente")
#         )

#         return reverse_lazy(
#             "evaluations_krm:ga_evaluation_residual_list"
#         )
