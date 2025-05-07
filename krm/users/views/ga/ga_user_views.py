from datetime import datetime
from django.urls import reverse
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect

import xlsxwriter
from django.http import HttpResponse

from django.contrib import messages
# import pandas as pd

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    RedirectView
)

from django.contrib.auth.decorators import login_required

from krm.users.decorators import (
    is_company_admin,
    is_global_admin
)

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.models.control_test_model import ControlTest
from krm.evaluations.models.evaluation_model import Evaluation
from krm.evaluations_krm.models.evaluation_krm_inherent_model import EvaluationKrmInherent
from krm.evaluations_krm.models.evaluation_krm_residual_model import EvaluationKrmResidual
from krm.evaluations_krm.models.risk_test_inherent_model import RiskTestInherent
from krm.evaluations_krm.models.risk_test_residual_model import RiskTestResidual

from krm.users.forms import LoginForm, RememberForm, PasswordForm, LoginCodeForm
from krm.users.models import User

from krm.evaluations.forms import EvaluationDashboardForm, DownloadEvaluationActionForm, EvaluationKrmDashboardForm

decorators = [
    csrf_protect,
    never_cache,
]


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaDashboardView(TemplateView, FormView):
    form_class = DownloadEvaluationActionForm

    def get_template_names(self):
        """
        Método de la vista que nos devuelve el nombre del template a usar en función de la elección del usuario
        a través de una request. Cada uno de los templates define un Dashboard diferente, conteniendo información
        distinta para cada uno de los casos.
        """
        dashboard= self.request.GET.get('dashboard', 'default')
        if dashboard == 'KRM':
            return ['dashboards/ga/GaDashboardKrm.html']
        else:
            return ['dashboards/ga/GaDashboard_copy.html']

    def get_context_data(self, **kwargs):
        """
        Método de la vista que, en función del template elegido por el usuario, envía datos para su visualización
        en gráficos.
        """
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [{'title': _('Dashboard'), 'url': reverse('users:ga_dashboard')},]
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        dashboard_type= self.request.GET.get('dashboard', 'default')
        context['dashboard']= dashboard_type
        get_data= self.request.GET.copy()
        get_data.pop('dashboard', None)

        if dashboard_type == 'KRM':
            context['page_title'] = _('Dashboard de Riesgos para el Administrador Global')
            if get_data:
               form = EvaluationKrmDashboardForm(get_data)
               context['search_evaluation_form']= form
            else:
                form = EvaluationKrmDashboardForm()
                context['search_evaluation_form'] = form
                context['evaluations_inherent'] = EvaluationKrmInherent.objects.all()
                context['evaluations_residual'] = EvaluationKrmResidual.objects.all()
                context['risk_test_inherent'] = RiskTestInherent.objects.all()
                context['risk_test_residual'] = RiskTestResidual.objects.all()

            if form.is_valid():
                cd= form.cleaned_data
                qs_inherent= EvaluationKrmInherent.objects.all()
                qs_residual= EvaluationKrmResidual.objects.all()
                test_inherent= RiskTestInherent.objects.all()
                test_residual= RiskTestResidual.objects.all()
                date_evaluation_begin = cd.get('date_evaluation_begin')
                date_evaluation_end = cd.get('date_evaluation_end')
                evaluation_inherent = cd.get('evaluation_inherent')
                evaluation_residual= cd.get('evaluation_residual')
                company = cd.get('company')
                certification_year = cd.get('certification_year')
                certification_period = cd.get('certification_period')
                status = cd.get('process_status')
                domain_risk= cd.get('domain_risk')

                if date_evaluation_begin != '' and date_evaluation_begin is not None:
                    date_evaluation_begin = datetime.strptime(date_evaluation_begin, '%d/%m/%Y')
                    qs_inherent = qs_inherent.filter(date_begin__gte=date_evaluation_begin)
                    qs_residual = qs_residual.filter(date_begin__gte=date_evaluation_begin)

                if date_evaluation_end != '' and date_evaluation_end is not None:
                    date_evaluation_end = datetime.strptime(date_evaluation_end, '%d/%m/%Y')
                    qs_inherent = qs_inherent.filter(date_end__lte=date_evaluation_end)
                    qs_residual = qs_residual.filter(date_end__lte=date_evaluation_end)

                if len(company) > 0:
                    qs_inherent = qs_inherent.filter(company__pk__in=company)
                    qs_residual = qs_residual.filter(company__pk__in=company)

                if len(evaluation_inherent) > 0:
                    qs_inherent = qs_inherent.filter(id__in=evaluation_inherent)
                if len(evaluation_residual) > 0:
                    qs_residual = qs_residual.filter(id__in=evaluation_residual)

                if len(certification_year) > 0:
                    qs_inherent = qs_inherent.filter(certification_year__in=certification_year)
                    qs_residual = qs_residual.filter(certification_year__in=certification_year)

                if len(certification_period) > 0:
                    qs_inherent = qs_inherent.filter(certification_period__in=certification_period)
                    qs_residual = qs_residual.filter(certification_period__in=certification_period)

                if len(status) > 0:
                    qs_inherent = qs_inherent.filter(status__in=status)
                    qs_residual = qs_residual.filter(status__in=status)

                if len(domain_risk) > 0:
                    qs_inherent = qs_inherent.filter(risk_test_inherents__risk__risk__risk_master__domain_risk__pk__in = domain_risk).distinct()
                    qs_residual = qs_residual.filter(risk_test_residuals__risk__risk__risk_master__domain_risk__pk__in = domain_risk).distinct()
                    test_inherent = test_inherent.filter(risk__risk__risk_master__domain_risk__pk__in=domain_risk, evaluation__in= qs_inherent)
                    test_residual = test_residual.filter(risk__risk__risk_master__domain_risk__pk__in=domain_risk, evaluation__in= qs_residual)
                else:
                    test_inherent = test_inherent.filter(evaluation__in= qs_inherent)
                    test_residual = test_residual.filter(evaluation__in= qs_residual)

                context['evaluations_inherent']= qs_inherent
                context['evaluations_residual']= qs_residual
                context['risk_test_inherent']= test_inherent
                context['risk_test_residual']= test_residual

        else:
            context['page_title'] = _('Dashboard de Controles para el Administrador Global')
            if get_data:
               form = EvaluationDashboardForm(self.request.GET)
               context['search_evaluation_form'] = form
            else:
                form = EvaluationDashboardForm()
                context['search_evaluation_form'] = form
                context['evaluations'] = Evaluation.objects.all()

            if form.is_valid():
                cd= form.cleaned_data
                qs= Evaluation.objects.all()
                date_evaluation_begin = cd.get('date_evaluation_begin')
                date_evaluation_end = cd.get('date_evaluation_end')
                evaluation = cd.get('evaluation')
                company = cd.get('company')
                certification_year = cd.get('certification_year')
                certification_period = cd.get('certification_period')
                status = cd.get('process_status')

                if date_evaluation_begin != '' and date_evaluation_begin is not None:
                    date_evaluation_begin = datetime.strptime(date_evaluation_begin, '%d/%m/%Y')
                    qs = qs.filter(date_begin__gte=date_evaluation_begin)

                if date_evaluation_end != '' and date_evaluation_end is not None:
                    date_evaluation_end = datetime.strptime(date_evaluation_end, '%d/%m/%Y')
                    qs = qs.filter(date_end__lte=date_evaluation_end)

                if len(company) > 0:
                    qs = qs.filter(company__pk__in=company)

                if len(evaluation) > 0:
                    qs = qs.filter(id__in=evaluation)

                if len(certification_year) > 0:
                    qs = qs.filter(certification_year__in=certification_year)

                if len(certification_period) > 0:
                    qs = qs.filter(certification_period__in=certification_period)

                if len(status) > 0:
                    qs = qs.filter(status__in=status)

                context['evaluations']= qs

        return context

    # def get_queryset(self):
    #     """
    #     Método de la vista que nos devuelve el queryset obtenido tras aplicar los filtros introducidos por el usuario
    #     desde la interfaz. En función del Dashboard que queramos visualizar nos encontraremos con unos filtros u otros.
    #     """
    #     qs = Evaluation.objects.filter(pk=-1)
    #     qs_control = ControlTest.objects.filter(pk=-1)
    #     if get_data:
    #         qs = Evaluation.objects.all()
    #         qs_control = ControlTest.objects.all()

    #         date_evaluation_begin = self.request.GET.get('date_evaluation_begin')
    #         date_evaluation_end = self.request.GET.get('date_evaluation_end')

    #         evaluation = self.request.GET.getlist('evaluation')
    #         company = self.request.GET.getlist('company')
    #         certification_year = self.request.GET.getlist('certification_year')
    #         certification_period = self.request.GET.getlist('certification_period')
    #         status = self.request.GET.getlist('process_status')
    #         control_status = self.request.GET.getlist('control_status')

    #         if date_evaluation_begin != '' and date_evaluation_begin is not None:
    #             date_evaluation_begin = datetime.strptime(
    #                 date_evaluation_begin, '%d/%m/%Y')
    #             qs = qs.filter(date_begin__gte=date_evaluation_begin)

    #         if date_evaluation_end != '' and date_evaluation_end is not None:
    #             date_evaluation_end = datetime.strptime(date_evaluation_end, '%d/%m/%Y')
    #             qs = qs.filter(date_end__lte=date_evaluation_end)

    #         # if date_created_begin != '' and date_created_begin is not None:
    #         #     date_created_begin = datetime.strptime(
    #         #         date_created_begin, '%d/%m/%Y')
    #         #     qs = qs.filter(created__gte=date_created_begin)

    #         # if date_created_end != '' and date_created_end is not None:
    #         #     date_created_end = datetime.strptime(
    #         #         date_created_end, '%d/%m/%Y')
    #         #     qs = qs.filter(created__lte=date_created_end)

    #         if len(company) > 0:
    #             qs = qs.filter(company__pk__in=company)

    #         if len(evaluation) > 0:
    #             qs = qs.filter(id__in=evaluation)

    #         if len(certification_year) > 0:
    #             qs = qs.filter(certification_year__in=certification_year)

    #         if len(certification_period) > 0:
    #             qs = qs.filter(certification_period__in=certification_period)

    #         if len(status) > 0:
    #             qs = qs.filter(status__in=status)

    #         if len(control_status) > 0:
    #             qs = qs_control.filter(status__in=control_status)

    #     else:
    #         qs = Evaluation.objects.all()

    #     return qs

    def form_valid(self, form):
        action = form.cleaned_data["action"]
        #from atenea.interactions.models.interaction_model import Interaction
        import io

        if action == 'download':
            filename = 'Dashboard results.xlsx'

            # Create an in-memory output file for the new workbook.
            output = io.BytesIO()

            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()

            # Add a bold format to use to highlight cells.
            bold = workbook.add_format({'bold': True})
            text_wrap = workbook.add_format({'text_wrap': True})

            columns = ['Evaluación',
                       'Control',
                       'Fecha de inicio',
                       'Supervisor',
                       'Control Owner',
                       'Status',
                       'Resultado'
                    ]

            for index, col_name in enumerate(columns):
                worksheet.write(0, index, col_name, bold)

            worksheet.set_column(0, 1, 25)
            worksheet.set_column(0, 2, 25)
            worksheet.set_column(0, 2, 25)
            worksheet.set_column(0, 3, 30)
            worksheet.set_column(0, 4, 75)
            worksheet.set_column(0, 5, 25)
            worksheet.set_column(0, 6, 25)

            row = 1
            for e in self.get_queryset():
                for ct in e.get_all_control_test_in_evaluation():

                    worksheet.write(row, 0, ct.evaluation.ref, text_wrap)
                    worksheet.write(row, 1, ct.control.ref, text_wrap)
                    worksheet.write(row, 2, ct.date_begin.strftime("%d-%m-%Y"), text_wrap)
                    worksheet.write(row, 3, ct.control_test_supervisor.full_name, text_wrap)
                    worksheet.write(row, 4, ct.control_test_owner.full_name, text_wrap)
                    worksheet.write(row, 5, ct.get_status_display(), text_wrap)
                    worksheet.write(row, 6, ct.get_result_display(), text_wrap)

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
