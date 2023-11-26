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
import pandas as pd

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

from krm.users.forms import LoginForm, RememberForm, PasswordForm, LoginCodeForm
from krm.users.models import User

from krm.evaluations.forms import EvaluationDashboardForm, DownloadEvaluationActionForm

decorators = [
    csrf_protect,
    never_cache,
]


@method_decorator([login_required, is_global_admin], name='dispatch')
class GaDashboardView(ListView, FormView):
    template_name = 'dashboards/ga/GaDashboard_copy.html'
    model = Evaluation
    context_object_name = 'evaluations'
    form_class = DownloadEvaluationActionForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:ga_dashboard')},
        ]
        context['page_title'] = _(
            'Dashboard para el Administrador Global')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        # df = pd.DataFrame(
        #     [{'tipo': 'Autopista', 'info': 'Third-party screening and due diligence', 'ref': 'USA-R07', 'x': 4.0, 'y': 3.0}, {'tipo': 'Autopista', 'info': 'Liability arising from employees ', 'ref': 'USA-R05', 'x': 3.0, 'y': 3.0}, {'tipo': 'Autopista', 'info': 'Financiación ilegal de partidos políticos', 'ref': 'GRU-R11', 'x': 3.2, 'y': 2.0}, {'tipo': 'Autopista', 'info': 'Malversación', 'ref': 'GRU-R28', 'x': 2.7, 'y': 2.3}, {'tipo': 'Autopista', 'info': 'Corrupción en los negocios', 'ref': 'GRU-R02', 'x': 3.1, 'y': 1.9}, {'tipo': 'Corporación', 'info': 'Cohecho', 'ref': 'GRU-R01', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Tráfico de Influencias', 'ref': 'GRU-R03', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Estafa', 'ref': 'GRU-R05', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Malversación', 'ref': 'GRU-R28', 'x': 4.0, 'y': 3.0}, {'tipo': 'Corporación', 'info': 'Mercado y Consumidores', 'ref': 'GRU-R07', 'x': 4.0, 'y': 2.0}, {'tipo': 'Corporación', 'info': 'Financiación ilegal de partidos políticos', 'ref': 'GRU-R11', 'x': 4.0, 'y': 2.0}, {'tipo': 'Corporación', 'info': 'Corrupción en los negocios', 'ref': 'GRU-R02', 'x': 2.5, 'y': 2.5}, {'tipo': 'Corporación', 'info': 'Descubrimiento y revelación de secretos', 'ref': 'GRU-R04', 'x': 2.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Falsificación de tarjetas de crédito, débito y cheques de viaje', 'ref': 'GRU-R14', 'x': 4.0, 'y': 4.0}, {'tipo': 'Ferrocarril', 'info': 'Cohecho', 'ref': 'GRU-R01', 'x': 4.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Tráfico de Influencias', 'ref': 'GRU-R03', 'x': 4.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Financiación ilegal de partidos políticos', 'ref': 'GRU-R11', 'x': 4.0, 'y': 3.0}, {'tipo': 'Ferrocarril', 'info': 'Malversación', 'ref': 'GRU-R28', 'x': 4.0, 'y': 3.0}, {'tipo': 'Innovación', 'info': 'Propiedad Industrial e Intelectual', 'ref': 'GRU-R18', 'x': 3.7, 'y': 3.0}, {'tipo': 'Innovación', 'info': 'Corrupción en los negocios', 'ref': 'GRU-R02', 'x': 3.8, 'y': 2.5}, {'tipo': 'Innovación', 'info': 'Liability arising from employees ', 'ref': 'USA-R05', 'x': 3.0, 'y': 3.0}, {'tipo': 'Innovación', 'info': 'Descubrimiento y revelación de secretos', 'ref': 'GRU-R04', 'x': 3.4, 'y': 2.6}, {'tipo': 'Innovación', 'info': 'Blanqueo de capitales', 'ref': 'GRU-R10', 'x': 3.8, 'y': 2.2}]
        # )
        # df['severidad'] = df['x']*df['y']
        # df = df.sort_values('severidad', ascending=False)
        # context['df'] = df

        if self.request.GET:
            context['search_evaluation_form'] = EvaluationDashboardForm(
                self.request.GET)
        else:
            context['search_evaluation_form'] = EvaluationDashboardForm()
            context['evaluations'] = Evaluation.objects.all()
        
        return context
    
    def get_queryset(self):
        qs = Evaluation.objects.filter(pk=-1)
        qs_control = ControlTest.objects.filter(pk=-1)
        if self.request.GET:
            qs = Evaluation.objects.all()
            qs_control = ControlTest.objects.all()

            date_evaluation_begin = self.request.GET.get('date_evaluation_begin')
            date_evaluation_end = self.request.GET.get('date_evaluation_end')
            # date_created_begin = self.request.GET.get('date_created_begin')
            # date_created_end = self.request.GET.get('date_created_end')

            evaluation = self.request.GET.getlist('evaluation')
            company = self.request.GET.getlist('company')
            certification_year = self.request.GET.getlist('certification_year')
            certification_period = self.request.GET.getlist('certification_period')
            # company = self.request.GET.getlist('company')
            status = self.request.GET.getlist('process_status')
            control_status = self.request.GET.getlist('control_status')

            if date_evaluation_begin != '' and date_evaluation_begin is not None:
                date_evaluation_begin = datetime.strptime(
                    date_evaluation_begin, '%d/%m/%Y')
                qs = qs.filter(date_begin__gte=date_evaluation_begin)

            if date_evaluation_end != '' and date_evaluation_end is not None:
                date_evaluation_end = datetime.strptime(date_evaluation_end, '%d/%m/%Y')
                qs = qs.filter(date_end__lte=date_evaluation_end)

            # if date_created_begin != '' and date_created_begin is not None:
            #     date_created_begin = datetime.strptime(
            #         date_created_begin, '%d/%m/%Y')
            #     qs = qs.filter(created__gte=date_created_begin)

            # if date_created_end != '' and date_created_end is not None:
            #     date_created_end = datetime.strptime(
            #         date_created_end, '%d/%m/%Y')
            #     qs = qs.filter(created__lte=date_created_end)

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
            
            if len(control_status) > 0:
                qs = qs_control.filter(status__in=control_status)

            # if len(phase) > 0:
            #     qs = qs.filter(phase__in=phase)
        else:
            qs = Evaluation.objects.all()

        return qs
    
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
