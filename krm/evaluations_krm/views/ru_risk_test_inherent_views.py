
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
from django.forms.models import model_to_dict

from django.shortcuts import get_object_or_404

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from krm.evaluations_krm.models.risk_test_inherent_model import RiskTestInherent
from krm.evaluations_krm.models import EvaluationKrmInherent

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import (
    EvaluationKrmInherent,
)

from krm.evaluations_krm.forms import (
    EvaluationInherenetCompleteForm,
)

from krm.evaluations.forms.evaluation_forms import (
    EvaluationActionForm,
)


@method_decorator((login_required, ), name="dispatch")
class RuEvaluationRiskInherentList(TemplateView):
    template_name = 'evaluations_krm/RuEvaluationKrmInherentList.html'

    def get_context_data(self, **kwargs):
        from datetime import date
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente')}
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Inherente')
        context['breadcrums'] = breadcrums

        ev_pending = self.request.user.evaluation_krm_inherent_pending()
        ev_delivered = self.request.user.evaluation_krm_inherent_delivered()
        ev_finished = self.request.user.evaluation_krm_inherent_finished()

        for ev in ev_pending:
            ev.nrisk_test_inherents_pending_user = ev.nrisk_test_inherents_by_state(1, self.request.user)
        for ev in ev_delivered:
            ev.nrisk_test_inherents_delivered_user = ev.nrisk_test_inherents_by_state(2, self.request.user)
        for ev in ev_finished:
            ev.nrisk_test_inherents_finished_user = ev.nrisk_test_inherents_by_state(3, self.request.user)

        eri_count_by_state_perc = {'FI': 0, 'EP': 0}

        if ev_delivered.count() != 0 or ev_pending.count() != 0:
            eri_count_by_state_perc['FI'] = int(
                100*ev_delivered.count()/(ev_delivered.count() + ev_pending.count()))
            eri_count_by_state_perc['EP'] = int(
                100*ev_pending.count()/(ev_delivered.count() + ev_pending.count()))

        context['eri_count_by_state_perc'] = eri_count_by_state_perc
        context['evaluations_risk_inherent_pending'] = ev_pending
        context['evaluations_risk_inherent_delivered'] = ev_delivered
        context['evaluations_risk_inherent_finished'] = ev_finished
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator((login_required, ), name="dispatch")
class RuEvaluationRiskInherentComplete(DetailView, FormView):
    template_name = 'evaluations_krm/RuEvaluationRiskInherentComplete.html'
    model = EvaluationKrmInherent
    context_object_name = 'evaluation'
    form_class = EvaluationInherenetCompleteForm

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().risk_test_inherents.filter(
            expert=request.user,
            status=1
        ).count() == 0:
            return HttpResponseRedirect(reverse_lazy(
                "evaluations_krm:ru_evaluation_risk_inherent_list"
            ))

        return super(RuEvaluationRiskInherentComplete, self).dispatch(
            request, request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente')}
        ]
        context['page_title'] = f"{_('Evaluación de Riesgo Inherente')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        risk_tests = self.object.risk_test_inherents.filter(
            expert=self.request.user,
            status=1
        )

        context['risks_test_inherent'] = risk_tests

        return context

    def form_valid(self, form):
        evaluation = self.get_object()
        RiskTestInherent.objects.filter(
            evaluation=evaluation,
            expert=self.request.user
        ).update(
            status=2
        )
        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Valoración de tests de Riesgo Inherente enviada correctamente")
        )

        return reverse_lazy(
            "evaluations_krm:ru_evaluation_risk_inherent_list"
        )


@method_decorator((login_required, ), name="dispatch")
class RuEvaluationRiskInherentDetail(FormView):
    template_name = 'evaluations_krm/RuEvaluationInherentDetail.html'
    form_class = EvaluationActionForm

    def dispatch(self, request, *args, **kwargs):
        evaluation_krm = get_object_or_404(
            EvaluationKrmInherent, pk=self.kwargs.get("pk"))
        self.evaluation = evaluation_krm
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['evaluation'] = self.evaluation
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones KRM'), 'url': reverse(
                'evaluations_krm:ru_evaluation_risk_inherent_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación KRM Inherent')} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums

        context['evaluation'].nrisk_test_inherents_pending = context['evaluation'].nrisk_test_inherents_by_state(1, user=self.request.user)
        context['evaluation'].nrisk_test_inherents_delivered = context['evaluation'].nrisk_test_inherents_by_state(2, user=self.request.user)
        context['evaluation'].nrisk_test_inherents_finished = context['evaluation'].nrisk_test_inherents_by_state(3, user=self.request.user)
        context['evaluation'].sev_not_stablished = context['evaluation'].nrisk_test_inherents_by_severity('SE', user= self.request.user)
        context['evaluation'].sev_very_low = context['evaluation'].nrisk_test_inherents_by_severity('MB', user= self.request.user)
        context['evaluation'].sev_low = context['evaluation'].nrisk_test_inherents_by_severity('B', user= self.request.user)
        context['evaluation'].sev_medium = context['evaluation'].nrisk_test_inherents_by_severity('M', user= self.request.user)
        context['evaluation'].sev_high = context['evaluation'].nrisk_test_inherents_by_severity('A', user= self.request.user)
        context['evaluation'].sev_very_high = context['evaluation'].nrisk_test_inherents_by_severity('MA', user= self.request.user)
        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        context['rit'] = RiskTestInherent.objects.filter(evaluation = self.evaluation, expert = self.request.user)
        context['rit_dict'] = []

        for risk_test in context['rit']:
            information = {}
            information['ref']= risk_test.risk.risk.ref
            information['name']= risk_test.risk.risk.name
            information['evaluator']= risk_test.expert.username_no_domain
            information['impact_evaluator']= risk_test.impact_level_expert
            information['probability_evaluator']= risk_test.probability_level_expert
            information['severity_evaluator']= risk_test.severity_level_expert
            information['administrator']= self.evaluation.admin_supervisor.username_no_domain if self.evaluation.admin_supervisor else ''
            information['impact_administrator']= risk_test.impact_level_administrator
            information['probability_administrator']= risk_test.probability_level_administrator
            information['severity_administrator']= risk_test.severity_level_administrator
            context['rit_dict'].append(information)

        if self.evaluation.admin_supervisor:
            context['rit_dict'] = sorted(context['rit_dict'], key=lambda x: x['severity_administrator'], reverse=False)
        else:
            context['rit_dict'] = sorted(context['rit_dict'], key=lambda x: x['severity_evaluator'], reverse=False)

        # Errores de encoding caracteres portugueses y españoles
        # for i,m in enumerate(context['rit_dict']):
        #     for k in m:
        #         if type(context['rit_dict'][i][k]) == str:
        #             context['rit_dict'][i][k] = context['rit_dict'][i][k].encode('utf-8').decode('utf-8')

        # JSON DUMP
        context['rit_json'] = json.dumps(context['rit_dict'], default=str,ensure_ascii=True)
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
            "evaluations_krm:ru_evaluation_krm_inherent_detail",
            kwargs={"pk": self.evaluation.pk},
        )
