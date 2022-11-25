from django.db.models import Count
from openpyxl import load_workbook
from io import BytesIO

import re

# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.forms import formset_factory

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

from django.utils.decorators import method_decorator

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.questionnaires.forms import (
    QuestionnaireCreateForm,
)

from krm.questionnaires.models import Questionnaire

from krm.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionnaireListView(ListView):
    model = Questionnaire
    template_name = 'questionnaires/GaQuestionnaireList.html'
    context_object_name = 'questionnaires'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
        ]
        context['page_title'] = _('Cuestionarios')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('questionnaires:ga_questionnaire_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionnaireDetailView(DetailView):
    model = Questionnaire
    template_name = 'questionnaires/GaQuestionnaireDetail.html'
    context_object_name = 'questionnaire'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            {'title': self.object.name}
        ]
        context['page_title'] = f"{_('Cuestionario')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('questionnaires:ga_questionnaire_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionnaireCreateView(CreateView):
    form_class = QuestionnaireCreateForm
    model = Questionnaire
    template_name = 'questionnaires/GaQuestionnaireCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            {'title': _('Nuevo Cuestionario'), 'url': reverse(
                'questionnaires:ga_questionnaire_create')},
        ]
        context['page_title'] = _('Nuesvo Cuestionario')
        context['breadcrums'] = breadcrums
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Cuestionario creada correctamente')
        )

        return reverse_lazy(
            'questionnaires:ga_questionnaire_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionnaireUpdateView(UpdateView):
    form_class = QuestionnaireCreateForm
    model = Questionnaire
    template_name = 'questionnaires/GaQuestionnaireCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Cuestionario')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Cuestionario actualizado correctamente')
        )
        return reverse_lazy(
            'questionnaires:ga_questionnaire_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionnaireDeleteView(DeleteView):
    model = Questionnaire
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Cuestionario")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Cuestionario eliminado correctamente")
        )
        return reverse_lazy("questionnaires:ga_questionnaire_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el cuestionario y todas sus evaluaciónes?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object))
