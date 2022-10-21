

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
            {'title': _('Evaluaciones de Riesgo Inherente asignadas')}
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Inherente asignadas')
        context['breadcrums'] = breadcrums

        evaluations_risk_inherent = EvaluationKrmInherent.objects.filter(
            risk_test_inherents__expert=self.request.user,
            risk_test_inherents__status=1
        ).filter(risk_test_inherents__status=1).distinct()

        eri_count_by_state = {
            'FI': 0,
            'EP': 0,
            }
        for ev in evaluations_risk_inherent:             
            eri_count_by_state[ev.status] += 1

        eri_count_by_state_perc = {
            'FI': int(100*eri_count_by_state['FI']/(eri_count_by_state['EP']+eri_count_by_state['FI'])),
            'EP': int(100*eri_count_by_state['EP']/(eri_count_by_state['EP']+eri_count_by_state['FI'])),
        }
            
        context['eri_count_by_state'] = {
            'perc': eri_count_by_state_perc,
            'val': eri_count_by_state,
            }
        context['evaluations_risk_inherent'] = evaluations_risk_inherent
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator((login_required, ), name="dispatch")
class RuEvaluationRiskInherentComplete(DetailView, FormView):
    template_name = 'evaluations_krm/RuEvaluationRiskInherentComplete.html'
    model = EvaluationKrmInherent
    context_object_name = 'evaluation'
    form_class = EvaluationInherenetCompleteForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente')}
        ]
        context['page_title'] = f"{_('Evaluación de Riesgos Inherentes')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['risks_test_inherent'] = self.object.risk_test_inherents.filter(
            expert=self.request.user
        )
        
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

# @method_decorator(login_required, name="dispatch")
# class RuControlTestOwnerList(TemplateView):
#     template_name = "control_tests/ru/RuControlTestOwnerList.html"

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context = KTLayout.init(context)
#         breadcrums = [
#             {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
#             {'title': _('Control Test para supervisar'), 'url': reverse(
#                 'control_tests:ru_control_test_supervisor_list')}
#         ]
#         context['page_title'] = _('Control Tests asignados como Control Owner')
#         context['breadcrums'] = breadcrums

#         context["control_test_pending"] = self.request.user.controls_test_owner.filter(
#             status="WO"
#         )
#         context["control_test_revision"] = self.request.user.controls_test_owner.filter(
#             status="WS"
#         )
#         context["control_test_administrator"] = self.request.user.controls_test_owner.filter(
#             status="WA"
#         )
#         context["control_test_finished"] = self.request.user.controls_test_owner.filter(
#             status="FI"
#         )
#         context['js_template'] = ['js/custom/datatables.js']

#         return context
