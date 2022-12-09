from django.db.models import Count
from openpyxl import load_workbook
from io import BytesIO
import uuid
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
    QuestionnaireImportForm
)
from krm.users.models import User

from krm.questionnaires.models import (
    Question,
    Questionnaire
)

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


@method_decorator([is_global_admin, ], name='dispatch')
class GaQuestionnaireImport(FormView):
    template_name = "questionnaires/GaQuestionnaireImport.html"
    form_class = QuestionnaireImportForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluaciones de Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
        ]
        context['page_title'] = _('Importar Cuestionario')
        context['breadcrums'] = breadcrums

        return context

    def form_valid(self, form):
        questions_to_create = []

        questionnaire_ref = form.cleaned_data["ref"]
        if Questionnaire.objects.filter(ref=questionnaire_ref).count() > 0:
            questionnaire_ref = f'{questionnaire_ref} - {uuid.uuid4().hex}'

        questionnaire_name = form.cleaned_data["name"]
        if Questionnaire.objects.filter(name=questionnaire_name).count() > 0:
            questionnaire_name = f'{questionnaire_name} - {uuid.uuid4().hex}'

        questionnaire = Questionnaire.objects.create(
            ref=questionnaire_ref,
            name=questionnaire_name
        )

        input_excel = self.request.FILES['questionnaire_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)
        sheet = wb.active

        nrow = 0
        rows = sheet.rows
        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            question = {}
            # Comprobamos que hay contenido en todas las celdas obligatorias
            if row[3].value is None or row[4] is None:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la fila %s falta algún campo obligatorio. Se ha abortado la importación') % str(
                            nrow+1)
                    )
                )
                return super(
                    GaQuestionnaireImport,
                    self
                ).form_invalid(form)
                break

            """
                0   DELEGACION
                1   CONCESION
                2   AREA
                3   REF
                4   PREGUNTA
                5   USUARIO/EMAIL
            """

            question['delegation'] = str(row[0].value).title()
            question['concession'] = str(row[1].value).title()
            question['area'] = str(row[2].value).title()
            question['ref'] = str(row[3].value)
            question['title'] = str(row[4].value)
            if row[5].value is not None:
                question['user'] = str(row[5].value).replace(' ', '')
            else:
                question['user'] = None
            if row[6].value is not None:
                question['order'] = int(row[6].value)
            else:
                question['order'] = 1

            # Tenemos que comprobar que el email esté bien formado
            if question['user'] is not None:
                question['user'] = question['user'].split(',')
                for email_user in question['user']:
                    if not re.match(
                        '^[(a-z0-9\_\-\.)]+@[(a-z0-9\_\-\.)]+\.[(a-z)]{2,4}$',
                        email_user.lower()
                    ):
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la fila %s el email introducido no es correcto. Se ha abortado la importación') % str(
                                    nrow+1)
                            )
                        )
                        return super(
                            GaQuestionnaireImport,
                            self
                        ).form_invalid(form)
                        break
                    if User.objects.filter(email=email_user).count() == 0:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la fila %s el email introducido no corresponde a ningún usuario dado de alta') % str(
                                    nrow+1)
                            )
                        )
                        return super(
                            GaQuestionnaireImport,
                            self
                        ).form_invalid(form)
                        break

            nrow += 1

            questions_to_create.append(question)

        questions_created = 0
        for q in questions_to_create:
            new_question = Question.objects.create(
                ref=q['ref'],
                questionnaire=questionnaire,
                delegation=q['delegation'],
                concession=q['concession'],
                area=q['area'],
                title=q['title'],
                order=q['order']
            )
            if q['user'] is not None:
                for user_email in q['user']:
                    new_question.user_to_assign.add(
                        User.objects.get(email=user_email))

            questions_created += 1

        messages.add_message(
            self.request,
            messages.SUCCESS,
            (_(f"Cuestionario {questionnaire.name} importado correctamente con {questions_created} preguntas")),
        )

        return super(GaQuestionnaireImport, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("questionnaires:ga_questionnaire_list")
