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

from krm.questionnaires.models import QuestionTest

from krm.evaluations.forms import (
    EvaluationActionForm
)

from krm.users.decorators import is_global_admin, user_can_view_evaluation

from krm.utils.utils import clean_html


@method_decorator([login_required, ], name='dispatch')
class RuEvaluationQuestionnaireListView(ListView):
    model = EvaluationQuestionnaire
    template_name = 'evaluation_questionnaires/RuEvaluationQuestionnaireList.html'
    # context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Cuestionsrios de Compliance'), 'url': reverse(
                'evaluation_questionnaires:ru_evaluation_questionnaire_list')},
        ]
        context['page_title'] = _('Evaluaciones de Cuestionarios de Compliance')
        context['breadcrums'] = breadcrums

        evaluations_pending = EvaluationQuestionnaire.objects.filter(
            question_tests__evaluator=self.request.user,
            question_tests__status=1,
            status='EP'
        ).distinct()

        evaluations_delivered = EvaluationQuestionnaire.objects.filter(
            question_tests__evaluator=self.request.user,
            question_tests__status=2,
            status='EP'
        ).distinct()

        evaluations_finished = EvaluationQuestionnaire.objects.filter(
            question_tests__evaluator=self.request.user,
            status='FI'
        ).distinct()

        for ev in evaluations_pending:
            ev.nquestion_test_pending_user = ev.nquestion_test_by_state(1, self.request.user)
        for ev in evaluations_delivered:
            ev.nquestion_test_delivered_user = ev.nquestion_test_by_state(2, self.request.user)
        for ev in evaluations_finished:
            ev.nquestion_test_finished_user = ev.nquestion_test_by_state(2, self.request.user)

        context['evaluations_pending'] = evaluations_pending
        context['evaluations_delivered'] = evaluations_delivered
        context['evaluations_finished'] = evaluations_finished

        return context


@method_decorator([login_required, ], name='dispatch')
class RuEvaluationQuestionnaireCompleteView(DetailView, FormView):
    template_name = 'evaluation_questionnaires/RuEvaluationQuestionnaireComplete.html'
    model = EvaluationQuestionnaire
    context_object_name = 'evaluation'
    form_class = EvaluationResidualCompleteForm

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().question_tests.filter(
            evaluator=request.user,
            status=1
        ).count() == 0:
            return HttpResponseRedirect(reverse_lazy(
                "evaluation_questionnaires:ru_evaluation_questionnaire_list"
            ))

        return super(RuEvaluationQuestionnaireCompleteView, self).dispatch(
            request, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluación de Cuestionario de Compliance'), 'url': reverse(
                'evaluation_questionnaires:ru_evaluation_questionnaire_list')},
            {'title': self.object.ref}
        ]
        context['page_title'] = f"{_('Evaluación de Cuestionario')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['js_template'] = ['js/custom/datatables.js']

        context['questions'] = QuestionTest.objects.filter(
            evaluation=self.object,
            evaluator=self.request.user
        ).order_by('scope', 'question__ref')

        return context

    def form_valid(self, form):
        evaluation = self.get_object()
        QuestionTest.objects.filter(
            evaluation=evaluation,
            evaluator=self.request.user
        ).update(
            status=2
        )
        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Questionario enviado correctamente")
        )

        return reverse_lazy(
            "evaluation_questionnaires:ru_evaluation_questionnaire_list"
        )
