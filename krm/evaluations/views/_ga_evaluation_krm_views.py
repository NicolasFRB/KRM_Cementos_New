from django.shortcuts import render
from django.conf import settings

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
from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationActionForm, EvaluationTemplateAssignDownload
from krm.evaluations.models import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.forms import EvaluationCreateForm, EvaluationUpdateForm
# from krm.evaluations.forms import EvaluationTestTemplateAssignDownload

from krm.evaluations.models import EvaluationKrmInherent
from krm.companies.models import Company
from krm.controls.models import Control

from krm.evaluations.forms import (
    EvaluationInherentCreateForm,
)

from krm.users.models import User

from krm.users.decorators import is_global_admin, user_can_view_evaluation

from krm.utils.utils import clean_html


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationInherentListView(ListView):
    model = EvaluationKrmInherent
    template_name = 'evaluations/GaEvaluationInherentList.html'
    context_object_name = 'evaluations'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones KRM'), 'url': reverse(
                'evaluations:ga_evaluation_krm_list')},
        ]
        context['page_title'] = _('Evaluaciones KRM')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('evaluations:ga_evaluation_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([login_required, is_global_admin, ], name='dispatch')
class GaEvaluationInherentCreateView(FormView):
    form_class = EvaluationInherentCreateForm
    model = EvaluationKrmInherent
    template_name = 'evaluations/GaEvaluationInherentCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones KRM'), 'url': reverse(
                'evaluations:ga_evaluation_list')},
            {'title': _('Nuevo'), 'url': reverse(
                'evaluations:ga_evaluation_inherent_create')},
        ]
        context['page_title'] = _('Nueva Evaluación de Riesgo Inherente [KRM]')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']

        return context

    def get_success_url(self):

        return reverse_lazy(
            'evaluations:ga_evaluation_list'
        )

    def form_valid(self, form):
        controls_created = 0
        evaluations_created = 0

        risk_companies = Company.objects.filter(
            pk__in=(form.cleaned_data["risk_companies"]))

        # for company in companies:
        #     evaluation = Evaluation.objects.create(
        #         ref=f'{form.cleaned_data["ref"]} - {company.name}',
        #         company=company,
        #         description=form.cleaned_data["description"],
        #         date_begin=form.cleaned_data["date_begin"],
        #         date_intermediate=form.cleaned_data["date_intermediate"],
        #         date_end=form.cleaned_data["date_end"],
        #         certification_year=form.cleaned_data["certification_year"],
        #         certification_period=form.cleaned_data["certification_period"],
        #         allow_self_autosupervision=form.cleaned_data[
        #             "allow_self_autosupervision"
        #         ],
        #     )

        #     # Para cada evaluación hay que crear los test controls de los controles que se han pasado
        #     for control in controls:
        #         control_test = ControlTest.objects.create(
        #             evaluation=evaluation,
        #             control=control,
        #             date_begin=form.cleaned_data["date_begin"]
        #         )

        #         controls_created += 1

        #     evaluations_created += 1

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Evaluaciones creadas correctamente") % str(evaluations_created),
        )

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("%s Test de Control creados correctamente") % str(controls_created),
        )
        return super().form_valid(form)
