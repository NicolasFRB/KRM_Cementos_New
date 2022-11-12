import json

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
from django.forms.models import model_to_dict

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import (
    EvaluationKrmResidual,
    RiskTestResidual
)

from krm.evaluations_krm.forms import (
    EvaluationResidualCompleteForm,
)

from krm.evaluations.forms.evaluation_forms import (
    EvaluationActionForm, 
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


@method_decorator((login_required, ), name="dispatch")
class RuEvaluationRiskResidualDetail(FormView):
    template_name = 'evaluations_krm/RuEvaluationResidualDetail.html'
    form_class = EvaluationActionForm

    def dispatch(self, request, *args, **kwargs):
        evaluation_krm = get_object_or_404(
            EvaluationKrmResidual, pk=self.kwargs.get("pk"))
        self.evaluation = evaluation_krm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.evaluation
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones KRM'), 'url': reverse(
                'evaluations_krm:ru_evaluation_risk_residual_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación KRM Residual')} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums
        
        context['evaluation'].nrisk_test_residuals_pending = context['evaluation'].nrisk_test_residuals_by_state(1, user=self.request.user)
        context['evaluation'].nrisk_test_residuals_delivered = context['evaluation'].nrisk_test_residuals_by_state(2, user=self.request.user)
        context['evaluation'].nrisk_test_residuals_finished = context['evaluation'].nrisk_test_residuals_by_state(3, user=self.request.user)
        
        # Serializar Evaluation no incluye sus hijos :(
        # Busco los hijos
        context['rrt'] = RiskTestResidual.objects.filter(
            evaluation = self.evaluation,
            evaluator = self.request.user,
            )
        
        # Paso a dict para json
        context['rrt_dict'] = [model_to_dict(m) for m in context['rrt']]
        
        # MODEL_TO_DICT not getting properties :(
        # Get .probability_level_residual_evaluator
        # TBI for cuadratico :/
        # Los risk_inherent_test no tienen ref ni name, es heredado del risk_company
        for i,r1 in enumerate(context['rrt']):
            context['rrt_dict'][i]['risk_ref'] = r1.risk.risk.ref
            context['rrt_dict'][i]['risk_name'] = r1.risk.risk.name
            for r2 in context['rrt_dict']:
                if r1.id == r2['id']: r2['probability_level_residual_evaluator'] = r1.probability_level_residual_evaluator

        # Sort by severity for a nice plot
        context['rrt_dict'] = sorted(context['rrt_dict'], key= lambda x: (x['probability_level_residual_evaluator'], x['risk_ref']))

        # Errores de encoding caracteres portugueses y españoles
        for i,m in enumerate(context['rrt_dict']):
            for k in m:
                if type(context['rrt_dict'][i][k]) == str:
                    context['rrt_dict'][i][k] = context['rrt_dict'][i][k].encode('utf-8').decode('utf-8')

        # JSON DUMP
        context['rrt_json'] = json.dumps(
            context['rrt_dict'],
            default=str,
            ensure_ascii=True,
            )
        
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def form_valid(self, form):
        action = form.cleaned_data["action"]
        evaluation = self.evaluation

        # if action == "i":
        #     evaluation.status = "EP"
        #     evaluation.save()
        #     users_notificated = []
        #     for ct in evaluation.control_tests.all():
        #         ct.status = "WO"
        #         ct.save()
        #         if ct.control_test_owner not in users_notificated:
        #             users_notificated.append(ct.control_test_owner)
        #             ct.send_notification()

        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         _("Evaluación iniciada correctamente"),
        #     )
        # elif action == 'f':
        #     evaluation.status = "FI"
        #     evaluation.save()
        #     evaluation.control_tests.update(
        #         status='FI'
        #     )

        #     messages.add_message(
        #         self.request,
        #         messages.SUCCESS,
        #         _("Evaluación finalizada correctamente"),
        #     )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "evaluations_krm:ru_evaluation_krm_residual_detail",
            kwargs={"pk": self.evaluation.pk},
        )
