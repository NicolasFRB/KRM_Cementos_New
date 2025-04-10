from django.shortcuts import render
from django.conf import settings
import json
import uuid
import xlsxwriter

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
from django.forms.models import model_to_dict

from django.shortcuts import get_object_or_404
from django.http import HttpResponse

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationActionForm, EvaluationTemplateAssignDownload
from krm.evaluations.models import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations_krm.models import EvaluationKrmInherent
from krm.companies.models import Company

from krm.evaluations_krm.forms import (
    EvaluationInherentCreateForm,
)

from krm.users.models import User
from krm.risks.models import RiskCompany

from krm.evaluations_krm.models import RiskTestInherent
from krm.companies.models import CompanyDomainRiskExperts

from krm.users.decorators import (
    is_company_admin,
    user_can_view_evaluation_inherent
)

from krm.evaluations_krm.forms import (
    EvaluationInherenetCompleteForm,
    EvaluationInherentNotificationForm
)


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class CaEvaluationInherentListView(ListView):
    model = EvaluationKrmInherent
    template_name = 'evaluations_krm/CaEvaluationInherentList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente KRM'), 'url': reverse(
                'evaluations_krm:ca_evaluation_inherent_list')},
        ]
        context['page_title'] = _('Evaluaciones de Riesgo Inherente KRM')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluations_krm:ca_evaluation_inherent_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        ev_pending = EvaluationKrmInherent.objects.filter(
            status="EP", company__in=self.request.user.companies_admin.all())
        ev_finished = EvaluationKrmInherent.objects.filter(
            status="FI", company__in=self.request.user.companies_admin.all())

        for ev in ev_pending:
            ev.nrisk_test_inherents_pending = ev.nrisk_test_inherents_by_state(
                1)
            ev.nrisk_test_inherents_delivered = ev.nrisk_test_inherents_by_state(
                2)
            ev.nrisk_test_inherents_finished = ev.nrisk_test_inherents_by_state(
                3)

            ev.experts_pending = ev.get_experts_by_rit_state(1)
            ev.experts_delivered = ev.get_experts_by_rit_state(2)
            ev.experts_finished = ev.get_experts_by_rit_state(3)

            ev.total_experts = ev.experts_pending.count() + ev.experts_delivered.count() + \
                ev.experts_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        for ev in ev_finished:
            ev.nrisk_test_inherents_pending = ev.nrisk_test_inherents_by_state(
                1)
            ev.nrisk_test_inherents_delivered = ev.nrisk_test_inherents_by_state(
                2)
            ev.nrisk_test_inherents_finished = ev.nrisk_test_inherents_by_state(
                3)

            ev.experts_pending = ev.get_experts_by_rit_state(1)
            ev.experts_delivered = ev.get_experts_by_rit_state(2)
            ev.experts_finished = ev.get_experts_by_rit_state(3)

            ev.total_experts = ev.experts_pending.count() + ev.experts_delivered.count() + \
                ev.experts_finished.count()

            ev.domain_risks = ev.get_domain_risk_in_evaluation()

        context['evaluations_pending'] = ev_pending
        context['evaluations_finished'] = ev_finished
        context['js_template'] = ['js/custom/datatables.js']
        return context

    # def get_queryset(self):
    #     from krm.evaluations_krm.models import EvaluationKrmInherent
    #     return EvaluationKrmInherent.objects.filter(
    #         company__in=self.request.user.companies_admin.all()
    #     )


@method_decorator([login_required, is_company_admin, ], name='dispatch')
class CaEvaluationInherentCreateView(FormView):
    form_class = EvaluationInherentCreateForm
    model = EvaluationKrmInherent
    template_name = 'evaluations_krm/CaEvaluationInherentCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Riesgo Inherente KRM'), 'url': reverse(
                'evaluations:ca_evaluation_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluations_krm:ca_evaluation_inherent_create')},
        ]

        context['page_title'] = _('Nueva Evaluación de Riesgo Inherente [KRM]')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def get_success_url(self):

        return reverse_lazy(
            'evaluations_krm:ca_evaluation_inherent_list'
        )

    def form_valid(self, form):
        risk_tests__created = 0
        evaluations_created = 0
        evaluations = []

        print("POST data:", self.request.POST)
        risk_companies = json.loads(form.cleaned_data["risk_companies"])
        for rc in risk_companies:
            company = Company.objects.get(pk=rc['company_pk'])
            riskcompany_pks = []

            for rc in rc['risks']:
                riskcompany_pks.append(rc[0])
                risk_company = RiskCompany.objects.get(pk=(rc[0]))
                risk_company.expert = User.objects.get(
                    pk=rc[1]
                )
                risk_company.save()

            risks= RiskCompany.objects.filter(pk__in=(riskcompany_pks))

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
                RiskTestInherent.objects.create(
                    evaluation=evaluation,
                    risk=risk,
                    expert=risk.expert
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
                        rt.send_notification_expert('Initial notification')
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


@method_decorator([login_required, is_company_admin, user_can_view_evaluation_inherent], name='dispatch')
class CaEvaluationInherentDetailView(FormView):
    template_name = 'evaluations_krm/CaEvaluationInherentDetail.html'
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
            {'title': _('Evaluaciones de Riesgo Inherente KRM'), 'url': reverse(
                'evaluations_krm:ca_evaluation_inherent_list')},
            {'title': self.evaluation.ref}
        ]
        context['page_title'] = f"{_('Evaluación de Riesgo Inherente KRM')} : {self.evaluation.ref}"
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

        context['evaluation'].experts_pending = context['evaluation'].get_experts_by_rit_state(
            1)
        context['evaluation'].experts_delivered = context['evaluation'].get_experts_by_rit_state(
            2)
        context['evaluation'].experts_finished = context['evaluation'].get_experts_by_rit_state(
            3)

        context['evaluation'].total_experts = context['evaluation'].experts_pending.count(
        ) + context['evaluation'].experts_delivered.count() + context['evaluation'].experts_finished.count()

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
            for r2 in context['rit_dict']:
                if r1.id == r2['id']:
                    r2['severity_level_expert'] = r1.severity_level_expert

        # QUITAR RESTO DE ATTRIBUTES (solo dan problemas con el encoding)
        for i, r1 in enumerate(context['rit']):
            for k in context['rit_dict'][i].copy():
                if k not in ['risk_ref', 'risk_name', 'expert', 'impact_level_expert', 'probability_level_expert', 'severity_level_expert']:
                    del context['rit_dict'][i][k]

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

        if action == 'download':
            import io

            filename = f'inherent_evaluation_{evaluation.ref}.xlsx'

            # Create an in-memory output file for the new workbook.
            output = io.BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet('Evaluation')
            worksheet_2= workbook.add_worksheet('Inherent risk tests')

            #Añadimos formatos de escritura
            bold = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
            italic= workbook.add_format({'italic': True})
            text_wrap = workbook.add_format({'text_wrap': True, 'align': 'center', 'valign': 'vcenter'})
            colors_format= [workbook.add_format({'color': '#d9d3d2'}), workbook.add_format({'color': '#09ef0d'}), workbook.add_format({'color': '#e8ee0b'}), workbook.add_format({'color': '#fea227'}), workbook.add_format({'color': '#ff6e56'}), workbook.add_format({'color': '#f10606'})]

            evaluation_columns = [
                'Evaluation ID',
                'Company (ID)',
                'Company type',
                'Evaluation description',
                'Start date',
                'End date',
                'Certification year',
                'Certification period',
                'Evaluation status',
                'Company administrator'
            ]

            tests_columns=[
                "Associated risk",
                "Associated master risk",
                "Associated risk domain",
                "Risk's description",
                "Risk's main elements",
                "Risk's main events",
                "Risk's affected activity",
                "Risk's exposed staff",
                "Company risk evaluator",
                "Evaluator's impact assessment",
                "Evaluator's impact qualitative assessment",
                "Evaluator's probability assessment",
                "Evaluator's probability qualitative assessment",
                "Evaluator's severity assesment",
                "Evaluator's severity qualitative assesment",
                "Evaluator's speed of ocurrence assessment",
                "Evaluator's speed of ocurrence qualitative assessment",
                "Evaluator's  justification",
                "Administrator's impact assessment",
                "Administrator's impact qualitative assessment",
                "Administrator's probability assessment",
                "Administrator's probability qualitative assessment",
                "Administrator's severity assesment",
                "Administrator's severity qualitative assesment",
                "Administrator's speed of ocurrence assessment",
                "Administrator's speed of ocurrence qualitative assessment",
                "Administrator's  justification"
            ]

            for index, col_name in enumerate(evaluation_columns):
                worksheet.write(0, index, col_name, bold)

            for index, col_name in enumerate(tests_columns):
                worksheet_2.write(0, index, col_name, bold)

            #Evaluation's sheet column formats (NMB)
            worksheet.set_column('A:B', 25, text_wrap)  #Evaluation ID, Company (ID) column's format
            worksheet.set_column('C:C', 40, text_wrap) #Company type column format
            worksheet.set_column('D:D', 80, text_wrap)
            worksheet.set_column('E:J', 40, text_wrap)

            #Test's sheet column formats (NMB)
            worksheet_2.set_column('A:C', 25, text_wrap)
            worksheet_2.set_column('D:H', 60, text_wrap)
            worksheet_2.set_column('I:I', 50, text_wrap)
            worksheet_2.set_column('J:J', 30, text_wrap)
            worksheet_2.set_column('K:Q', 20, text_wrap)
            worksheet_2.set_column('R:R', 50, text_wrap)
            worksheet_2.set_column('S:Z', 20, text_wrap)
            worksheet_2.set_column('AA:AA', 50, text_wrap)

            #Writing on the fisrt sheet:
            worksheet.write(1, 0, evaluation.ref, text_wrap)
            worksheet.write(1, 1, evaluation.company.name +' (' + evaluation.company.ref+')' , text_wrap)
            worksheet.write(1, 2, evaluation.company.type_company if evaluation.company.type_company else "Not specified", text_wrap)
            worksheet.write(1, 3, evaluation.description if evaluation.description else "Not specified", text_wrap)
            worksheet.write(1, 4, evaluation.date_begin.strftime("%d/%m/%Y"), text_wrap)
            worksheet.write(1, 5, evaluation.date_end.strftime("%d/%m/%Y"), text_wrap)
            worksheet.write(1, 6, evaluation.certification_year, text_wrap)
            worksheet.write(1, 7, evaluation.certification_period if evaluation.certification_period else "Not specified", text_wrap)
            if evaluation.status== 'EP':
                worksheet.write(1, 8, "In progress", text_wrap)
            else:
                worksheet.write(1, 8, "Completed", text_wrap)
            worksheet.write(1, 9, evaluation.admin_supervisor.full_name if evaluation.admin_supervisor else "Awaiting evaluation", text_wrap)

            row = 1

            for rr in evaluation.risk_test_inherents.all():
                worksheet_2.write(row, 0, rr.risk.risk.name + ' ('+ rr.risk.risk.ref + ')', text_wrap)
                worksheet_2.write(row, 1, rr.risk.risk.risk_master.name + ' ('+ rr.risk.risk.risk_master.ref + ')', text_wrap)
                worksheet_2.write(row, 2, rr.risk.risk.risk_master.domain_risk.name + ' ('+ rr.risk.risk.risk_master.domain_risk.ref + ')', text_wrap)
                worksheet_2.write(row, 3, rr.risk.risk.description if rr.risk.risk.description else "Not specified", text_wrap)
                worksheet_2.write(row, 4, rr.risk.risk.krm_main_elements if rr.risk.risk.krm_main_elements!= '' else "N/A", text_wrap)
                worksheet_2.write(row, 5, rr.risk.risk.krm_main_events if  rr.risk.risk.krm_main_events!='' else "N/A", text_wrap)
                worksheet_2.write(row, 6, rr.risk.risk.krm_activity_affected if rr.risk.risk.krm_activity_affected!='' else "N/A", text_wrap)
                worksheet_2.write(row, 7, rr.risk.risk.krm_exposed_staff if rr.risk.risk.krm_exposed_staff!='' else "N/A", text_wrap)
                worksheet_2.write(row, 8, rr.risk.expert.full_name if rr.risk.evaluator else "Evaluator not assigned ", text_wrap)
                worksheet_2.write(row, 9, rr.impact_level_expert if rr.impact_level_expert!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 10, rr.translation_values(rr.impact_level_expert), text_wrap)
                worksheet_2.write(row, 11, rr.probability_level_expert if rr.probability_level_expert!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 12, rr.translation_values(rr.probability_level_expert), text_wrap)
                worksheet_2.write(row, 13, rr.severity_level_expert if rr.severity_level_expert!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 14, rr.qualitative_severity("en", "evaluator"), text_wrap)
                worksheet_2.write(row, 15, rr.event_speed_level_expert if rr.event_speed_level_expert!=0 else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 16, rr.translation_values(rr.event_speed_level_expert), text_wrap)
                worksheet_2.write(row, 17, rr.description_expert if rr.description_expert!='' else "Awaiting evaluation", text_wrap)
                worksheet_2.write(row, 18, rr.impact_level_administrator if rr.impact_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 19, rr.translation_values(rr.impact_level_administrator), text_wrap)
                worksheet_2.write(row, 20, rr.probability_level_administrator if rr.probability_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 21, rr.translation_values(rr.probability_level_administrator), text_wrap)
                worksheet_2.write(row, 22, rr.severity_level_administrator if rr.severity_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 23, rr.qualitative_severity("en", "administrator"), text_wrap)
                worksheet_2.write(row, 24, rr.event_speed_level_administrator if rr.event_speed_level_administrator!=0 else "Awaiting supervision", text_wrap)
                worksheet_2.write(row, 25, rr.translation_values(rr.event_speed_level_administrator), text_wrap)
                worksheet_2.write(row, 26, rr.description_administrator if rr.description_administrator else "Awaiting supervision", text_wrap)
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
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy(
            "evaluations_krm:ca_evaluation_inherent_detail",
            kwargs={"pk": self.evaluation.pk},
        )


@method_decorator([login_required, is_company_admin, user_can_view_evaluation_inherent], name='dispatch')
class CaEvaluationInherentAdminComplete(DetailView, FormView):
    template_name = 'evaluations_krm/CaEvaluationInherentAdminComplete.html'
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
        context['page_title'] = f"{_('Evaluación de Riesgo Inherente')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['risks_test_inherent'] = self.object.risk_test_inherents.filter()

        return context

    def form_valid(self, form):
        evaluation = self.get_object()
        risk_inherents = RiskTestInherent.objects.filter(
            evaluation=evaluation
        )
        for ri in risk_inherents:
            ri.status = 3
            if ri.probability_level_administrator == 0:
                ri.probability_level_administrator = ri.probability_level_expert
            if ri.impact_level_administrator == 0:
                ri.impact_level_administrator = ri.impact_level_expert
            if ri.event_speed_level_administrator == 0:
                ri.event_speed_level_administrator = ri.event_speed_level_expert
            if ri.description_administrator == '' or ri.description_administrator == None:
                ri.description_administrator = ri.description_expert
            ri.save()
        evaluation.status = 'FI'
        evaluation.admin_supervisor = self.request.user
        evaluation.save()
        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Evaluación supervisada correctamente como administrador de compañía")
        )

        return reverse_lazy(
            "evaluations_krm:ca_evaluation_inherent_list"
        )

@method_decorator([is_company_admin, ], name='dispatch')
class CaEvaluationInherentNotificationsView(DetailView, FormView):
    template_name = 'evaluations_krm/CaEvaluationInherentNotifications.html'
    model = EvaluationKrmInherent
    context_object_name = 'evaluation'
    form_class = EvaluationInherentNotificationForm

    def dispatch(self, request, *args, **kwargs):
        self.evaluation = get_object_or_404(
            EvaluationKrmInherent, pk=self.kwargs.get("pk"))
        return super(CaEvaluationInherentNotificationsView, self).dispatch(
            request, request, *args, **kwargs
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones KRM'), 'url': reverse(
                'evaluations_krm:ca_evaluation_inherent_list')},
            {'title': self.object.ref, 'url': reverse(
                "evaluations_krm:ca_evaluation_inherent_detail", kwargs={'pk': self.object.pk})}
        ]
        context['page_title'] = f"{_('Notificaciones de Riesgo Inherente')} : {self.object.ref}"
        context['breadcrums'] = breadcrums

        context['evaluation'].evaluators_notifications = context['evaluation'].get_evaluators_for_notifications()

        context['js_template'] = ['js/custom/datatables.js']

        return context

    def post(self, request, *args, **kwargs):
        risk_test_selected = request.POST.getlist('notify_pk')

        from krm.evaluations_krm.models import (
            RiskTestInherent,
        )

        for pk in risk_test_selected:
            rt = RiskTestInherent.objects.filter(pk = int(pk)).first()
            rt.send_notification_expert('Reminder')

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Enviadas notificaciones a %d usuarios!" % len(risk_test_selected))
        )

        return HttpResponseRedirect(
            reverse_lazy(
                "evaluations_krm:ca_evaluation_inherent_detail",
                kwargs={'pk': self.evaluation.pk}
            )
        )
