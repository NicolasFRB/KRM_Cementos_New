from django.shortcuts import render
from django.conf import settings
import json
import uuid

import re

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
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationActionForm, EvaluationTemplateAssignDownload
from krm.evaluations.models import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.forms import EvaluationCreateForm, EvaluationUpdateForm
# from krm.evaluations.forms import EvaluationTestTemplateAssignDownload

from krm.evaluations_krm.models import EvaluationKrmInherent
from krm.companies.models import Company

from krm.evaluations_krm.forms import (
    EvaluationInherentCreateForm,
)

from krm.risks.models import RiskCompany

from krm.evaluations_krm.models import RiskTestInherent
from krm.companies.models import CompanyDomainRiskExperts

from krm.users.decorators import is_global_admin, user_can_view_evaluation

from krm.utils.utils import clean_html


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationInherentListView(ListView):
    model = EvaluationKrmInherent
    template_name = 'evaluations_krm/GaEvaluationInherentList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente KRM'), 'url': reverse(
                'evaluations_krm:ga_evaluation_inherent_list')},
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Inherente KRM')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluations_krm:ga_evaluation_inherent_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]

        ev_pending = EvaluationKrmInherent.objects.filter(status="EP")
        ev_finished = EvaluationKrmInherent.objects.filter(status="FI")

        for ev in ev_pending:
            ev.nrisk_test_inherents_pending = ev.nrisk_test_inherents_by_state(1)
            ev.nrisk_test_inherents_delivered = ev.nrisk_test_inherents_by_state(2)
            ev.nrisk_test_inherents_finished = ev.nrisk_test_inherents_by_state(3)

            ev.experts_pending = ev.get_experts_by_rit_state(1)
            ev.experts_delivered = ev.get_experts_by_rit_state(2)
            ev.experts_finished = ev.get_experts_by_rit_state(3)

            ev.total_experts = ev.experts_pending.count() + ev.experts_delivered.count() + ev.experts_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        for ev in ev_finished:
            ev.nrisk_test_inherents_pending = ev.nrisk_test_inherents_by_state(1)
            ev.nrisk_test_inherents_delivered = ev.nrisk_test_inherents_by_state(2)
            ev.nrisk_test_inherents_finished = ev.nrisk_test_inherents_by_state(3)

            ev.experts_pending = ev.get_experts_by_rit_state(1)
            ev.experts_delivered = ev.get_experts_by_rit_state(2)
            ev.experts_finished = ev.get_experts_by_rit_state(3)

            ev.total_experts = ev.experts_pending.count() + ev.experts_delivered.count() + ev.experts_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        context['evaluations_pending'] = ev_pending
        context['evaluations_finished'] = ev_finished
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationInherentCreateView(FormView):
    form_class = EvaluationInherentCreateForm
    model = EvaluationKrmInherent
    template_name = 'evaluations_krm/GaEvaluationInherentCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente KRM'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluations_krm:ga_evaluation_inherent_create')},
        ]

        context['page_title'] = _('Nueva Evaluación de Riesgo Inherente [KRM]')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def get_success_url(self):

        return reverse_lazy(
            'evaluations_krm:ga_evaluation_inherent_list'
        )

    def form_valid(self, form):
        risk_tests__created = 0
        evaluations_created = 0
        evaluations = []

        risk_companies = json.loads(form.cleaned_data["risk_companies"])
        for rc in risk_companies:
            company = Company.objects.get(pk=rc['company_pk'])
            risks = RiskCompany.objects.filter(pk__in=(rc['risks']))

            if EvaluationKrmInherent.objects.filter(
                ref=f'{form.cleaned_data["ref"]} - {company.name}',
            ).count() > 0:
                ref = f'{form.cleaned_data["ref"]} - {company.name} - {uuid.uuid4().hex}'
            else:
                ref = f'{form.cleaned_data["ref"]} - {company.name}'

            evaluation = EvaluationKrmInherent.objects.create(
                ref=ref,
                company=company,
                description=form.cleaned_data["description"],
                date_begin=form.cleaned_data["date_begin"],
                date_end=form.cleaned_data["date_end"],
                certification_year=form.cleaned_data["certification_year"],
                certification_period=form.cleaned_data["certification_period"]
            )

            evaluations.append(evaluation)

            # Para cada evaluación hay que crear los test controls de los controles que se han pasado
            for risk in risks:
                company_expert = CompanyDomainRiskExperts.objects.get(
                    company=company,
                    domain_risk=risk.risk.risk_master.domain_risk
                )
                RiskTestInherent.objects.create(
                    evaluation=evaluation,
                    risk=risk,
                    expert=company_expert.expert
                )

                risk_tests__created += 1

            evaluations_created += 1

            # En este caso se puede iniciar ya la evaluación
            users_notificated = []
            for e in evaluations:
                for rt in e.risk_test_inherents.all():
                    rt.status = 1
                    rt.save()
                    if rt.expert not in users_notificated:
                        rt.send_notification_expert()
                        users_notificated.append(rt.expert)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Evaluaciones creadas correctamente") % str(evaluations_created),
        )

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Test de Riesgos creados correctamente") % str(
                risk_tests__created),
        )
        return super().form_valid(form)


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationInherentDetailView(FormView):
    template_name = 'evaluations_krm/GaEvaluationInherentDetail.html'
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
                'evaluations_krm:ga_evaluation_inherent_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación KRM Inherent')} : {self.evaluation.ref}"
        context['breadcrums'] = breadcrums
        # context['actions'] = [
        #     {
        #         'title': _('Editar'),
        #         'url': reverse('evaluations:ga_evaluation_update', kwargs={'pk': self.evaluation.pk}),
        #         'primary': True,
        #         'icon': '<i class="bi bi-pencil"></i>'
        #     },
        # ]

        context['evaluation'].nrisk_test_inherents_pending = context['evaluation'].nrisk_test_inherents_by_state(
            1)
        context['evaluation'].nrisk_test_inherents_delivered = context['evaluation'].nrisk_test_inherents_by_state(
            2)
        context['evaluation'].nrisk_test_inherents_finished = context['evaluation'].nrisk_test_inherents_by_state(
            3)

        context['evaluation'].experts_pending = context['evaluation'].get_experts_by_rit_state(1)
        context['evaluation'].experts_delivered = context['evaluation'].get_experts_by_rit_state(2)
        context['evaluation'].experts_finished = context['evaluation'].get_experts_by_rit_state(3)

        context['evaluation'].total_experts = context['evaluation'].experts_pending.count() + context['evaluation'].experts_delivered.count() + context['evaluation'].experts_finished.count()

        context['evaluation'].domain_risks = context['evaluation'].get_domain_risk_in_evaluation()

        # Serializar Evaluation no incluye sus hijos :(
        # Busco los hijos
        context['rit'] = RiskTestInherent.objects.filter(
            evaluation=self.evaluation)

        # Paso a dict para json
        context['rit_dict'] = [model_to_dict(m) for m in context['rit']]

        # MODEL_TO_DICT not getting properties :(
        # Get .severity_level_expert
        # TBI for cuadratico :/
        # Los risk_inherent_test no tienen ref ni name, es heredado del risk_company
        for i, r1 in enumerate(context['rit']):
            context['rit_dict'][i]['risk_ref'] = r1.risk.risk.ref
            context['rit_dict'][i]['risk_name'] = r1.risk.risk.name
            context['rit_dict'][i]['expert'] = r1.expert.username_no_domain
            for r2 in context['rit_dict']:
                if r1.id == r2['id']:
                    r2['severity_level_expert'] = r1.severity_level_expert
                    

        # Sort by severity for a nice plot
        context['rit_dict'] = sorted(context['rit_dict'], key=lambda x: (
            x['severity_level_expert'], x['risk_ref']), reverse=True)

        # Errores de encoding caracteres portugueses y españoles
        for i, m in enumerate(context['rit_dict']):
            for k in m:
                if type(context['rit_dict'][i][k]) == str:
                    context['rit_dict'][i][k] = context['rit_dict'][i][k].encode(
                        'utf-8').decode('utf-8')

        # JSON DUMP
        context['rit_json'] = json.dumps(
            context['rit_dict'],
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
            "evaluations_krm:ga_evaluation_krm_inherent_detail",
            kwargs={"pk": self.evaluation.pk},
        )
