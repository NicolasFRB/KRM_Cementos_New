

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
from krm.evaluations_krm.models.risk_test_inherent_model import RiskTestInherent

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import (
    EvaluationKrmInherent,
)

from krm.evaluations_krm.forms import (
    EvaluationInherenetCompleteForm,
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
            ev.nrisk_test_inherents_pending_user = ev.nrisk_test_inherents_pending_user(
                self.request.user)
        for ev in ev_delivered:
            ev.nrisk_test_inherents_delivered_user = ev.nrisk_test_inherents_delivered_user(
                self.request.user)
        for ev in ev_finished:
            ev.nrisk_test_inherents_finished_user = ev.nrisk_test_inherents_finished_user(
                self.request.user)

        eri_count_by_state_perc = {
            'FI': int(100*ev_delivered.count()/(ev_delivered.count() + ev_pending.count())),
            'EP': int(100*ev_pending.count()/(ev_delivered.count() + ev_pending.count())),
        }

        if ev_delivered or ev_pending:
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
        context['page_title'] = f"{_('Evaluación de Riesgos Inherentes')} : {self.object.ref}"
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
                "Evaluación enviada para validar correctamente")
        )

        return reverse_lazy(
            "evaluations_krm:ru_evaluation_risk_inherent_list"
        )
