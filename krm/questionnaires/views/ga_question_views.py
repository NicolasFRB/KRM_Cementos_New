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
    QuestionCreateForm,
)

from krm.questionnaires.models import Question, Questionnaire

from krm.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionListView(ListView):
    model = Question
    template_name = 'questions/GaQuestionList.html'
    context_object_name = 'questions'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Preguntas'), 'url': reverse(
                'questions:ga_question_list')},
        ]
        context['page_title'] = _('Preguntas')
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Nuevo'),
                'url': reverse('questions:ga_question_create'),
                'primary': True,
                'icon': '<i class="bi bi-plus-lg"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionDetailView(DetailView):
    model = Question
    template_name = 'questions/GaQuestionDetail.html'
    context_object_name = 'question'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Preguntas'), 'url': reverse(
                'questions:ga_question_list')},
            {'title': self.object.name}
        ]
        context['page_title'] = f"{_('Preguntas')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['actions'] = [
            {
                'title': _('Editar'),
                'url': reverse('questions:ga_question_update', kwargs={'pk': self.object.pk}),
                'primary': True,
                'icon': '<i class="bi bi-pencil"></i>'
            },
        ]
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionCreateView(CreateView):
    form_class = QuestionCreateForm
    model = Question
    template_name = 'questions/GaQuestionCreate.html'

    def get_initial(self):
        if 'questionnaire' in self.kwargs:
            questionnaire = get_object_or_404(
                Questionnaire, pk=self.kwargs.get('questionnaire')
            )
            return {
                'questionnaire': questionnaire
            }
        else:
            return {}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Preguntas'), 'url': reverse(
                'questions:ga_question_list')},
            {'title': _('Nueva pregunta'), 'url': reverse(
                'questions:ga_question_create')},
        ]
        context['page_title'] = _('Nueva pregunta')
        context['breadcrums'] = breadcrums
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Pregunta creada correctamente')
        )

        return reverse_lazy(
            'questionnaires:ga_questionnaire_detail',
            kwargs={'pk': self.object.questionnaire.pk}
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionUpdateView(UpdateView):
    form_class = QuestionCreateForm
    model = Question
    template_name = 'questions/GaQuestionCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Preguntas'), 'url': reverse(
                'questions:ga_question_list')},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Pregunta')
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Pregunta actualizada correctamente')
        )
        return reverse_lazy(
            'questions:ga_question_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionDeleteView(DeleteView):
    model = Question
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Preguntas'), 'url': reverse(
                'questions:ga_question_list')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Pregunta")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Pregunta eliminada correctamente")
        )
        return reverse_lazy("questions:ga_question_list")

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el cuestionario y todas sus evaluaciónes?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object))
