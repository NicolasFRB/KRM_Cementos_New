

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render

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

from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import (
    EvaluationKrmResidual,
    RiskTestResidual
)

from krm.evaluations_krm.forms import (
    EvaluationResidualCompleteForm,
)


@method_decorator((login_required, ), name="dispatch")
class RuEvaluationRiskResidualList(TemplateView):
    template_name = 'evaluations_krm/RuEvaluationKrmResidualList.html'

    def get_context_data(self, **kwargs):
        from datetime import date
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual')}
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Residual')
        context['breadcrums'] = breadcrums

        ev_pending = self.request.user.evaluation_krm_residual_pending()
        ev_delivered = self.request.user.evaluation_krm_residual_delivered()
        ev_finished = self.request.user.evaluation_krm_residual_finished()

        for ev in ev_pending:
            ev.nrisk_test_residuals_pending_user = ev.nrisk_test_residuals_pending_user(
                self.request.user)
        for ev in ev_delivered:
            ev.nrisk_test_residuals_delivered_user = ev.nrisk_test_residuals_delivered_user(
                self.request.user)
        for ev in ev_finished:
            ev.nrisk_test_residuals_finished_user = ev.nrisk_test_residuals_finished_user(
                self.request.user)
        
        eri_count_by_state_perc = {'FI': 0, 'EP': 0}
        
        if ev_delivered.count() != 0 or ev_pending.count() != 0:
            eri_count_by_state_perc['FI'] = int(
                100*ev_delivered.count()/(ev_delivered.count() + ev_pending.count()))
            eri_count_by_state_perc['EP'] = int(
                100*ev_pending.count()/(ev_delivered.count() + ev_pending.count()))

        context['eri_count_by_state_perc'] = eri_count_by_state_perc
        context['evaluations_risk_residual_pending'] = ev_pending
        context['evaluations_risk_residual_delivered'] = ev_delivered
        context['evaluations_risk_residual_finished'] = ev_finished
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator((login_required, ), name="dispatch")
class RuEvaluationRiskResidualComplete(DetailView, FormView):
    template_name = 'evaluations_krm/RuEvaluationRiskResidualComplete.html'
    model = EvaluationKrmResidual
    context_object_name = 'evaluation'
    form_class = EvaluationResidualCompleteForm

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().risk_test_residuals.filter(
            evaluator=request.user,
            status=1
        ).count() == 0:
            return HttpResponseRedirect(reverse_lazy(
                "evaluations_krm:ru_evaluation_risk_residual_list"
            ))

        return super(RuEvaluationRiskResidualComplete, self).dispatch(
            request, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Residual')}
        ]
        context['page_title'] = f"{_('Evaluación de Riesgo Residuale')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        risk_tests = self.object.risk_test_residuals.filter(
            evaluator=self.request.user,
            status=1
        )

        for r in risk_tests:
            r.controls_attempt_to_mitigate = r.get_controls_attempt_to_mitigate()
            r.test_controls_attempt_to_mitigate = r.get_test_controls_attempt_to_mitigate()

        context['risks_test_residual'] = sorted(risk_tests, key=lambda t: t.get_latest_severity_inherent, reverse=True)

        return context

    def form_valid(self, form):
        evaluation = self.get_object()
        RiskTestResidual.objects.filter(
            evaluation=evaluation,
            evaluator=self.request.user
        ).update(
            status=2
        )
        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Evaluación enviada para validar correctamente")
        )

        return reverse_lazy(
            "evaluations_krm:ru_evaluation_risk_residual_list"
        )
