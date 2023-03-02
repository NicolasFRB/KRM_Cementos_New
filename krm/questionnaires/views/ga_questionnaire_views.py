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
    Questionnaire,
    Scope
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
    template_name = 'questionnaires/GaQuestionnaireUpdate.html'

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

        input_excel = self.request.FILES['questionnaire_file'].read()
        wb = load_workbook(filename=BytesIO(input_excel), data_only=True)

        # Questionnaires
        questionnaires_sheet = wb['QUESTIONNAIRES']
        questionnaires_to_create = []
        nrow = 0
        rows = questionnaires_sheet.rows
        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            questionnaire = {}
            # Comprobamos que hay contenido en todas las celdas obligatorias
            if row[0].value is None or row[1] is None:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de Cuestionarios, en la fila %s falta algún campo obligatorio. Se ha abortado la importación') % str(
                            nrow+1)
                    )
                )
                return super(
                    GaQuestionnaireImport,
                    self
                ).form_invalid(form)
                break

            """
                0   QUESTIONNAIRE_REF
                1   QUESTIONNAIRE_NAME
            """

            questionnaire['ref'] = str(row[0].value).replace(' ', '')
            questionnaire['name'] = str(row[1].value)

            # Comprobamos que no exista ya un cuestionario con esa referencia
            if Questionnaire.objects.filter(ref=questionnaire['ref']).count() > 0:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de Cuestionarios, en la fila %s ya existe un cuestionario con esa referencia. Se ha abortado la importación') % str(
                            nrow+1)
                    )
                )
                return super(
                    GaQuestionnaireImport,
                    self
                ).form_invalid(form)
                break

            nrow += 1
            questionnaires_to_create.append(questionnaire)

        # Scopes
        scopes_sheet = wb['SCOPES']
        scopes_to_create = []
        nrow = 0
        rows = scopes_sheet.rows
        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            scope = {}
            # Comprobamos que hay contenido en todas las celdas obligatorias
            if row[0].value is None or row[1] is None or row[2] is None:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la hoja de alcances, en la fila %s falta algún campo obligatorio. Se ha abortado la importación') % str(
                            nrow+1)
                    )
                )
                return super(
                    GaQuestionnaireImport,
                    self
                ).form_invalid(form)
                break

            """
                0   QUESTIONNAIRE_REF
                1   SCOPE_REF
                2   SCOPE_NAME
                3   USUARIO/EMAIL
            """

            scope['questionnaire_ref'] = str(row[0].value).replace(' ', '')
            # Comprobamos que el cuestionario existe
            if Questionnaire.objects.filter(ref=scope['questionnaire_ref']).count() == 0:
                if scope['questionnaire_ref'] not in [q['ref'] for q in questionnaires_to_create]:
                    messages.add_message(
                        self.request,
                        messages.ERROR,
                        (
                            _('En la hoja de alcances, en la fila %s no existe el cuestionario con esa referencia. Se ha abortado la importación') % str(
                                nrow+1)
                        )
                    )
                    return super(
                        GaQuestionnaireImport,
                        self
                    ).form_invalid(form)
                    break
            scope['ref'] = str(row[1].value).replace(' ', '')
            scope['name'] = str(row[2].value)
            if row[3].value is not None:
                scope['users'] = str(row[3].value).replace(' ', '')
            else:
                scope['users'] = None

            # Tenemos que comprobar que el email esté bien formado
            if scope['users'] is not None:
                scope['users'] = scope['users'].split(',')
                for email_user in scope['users']:
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
            scopes_to_create.append(scope)

        # Questions
        questions_sheet = wb['QUESTIONS']
        questions_to_create = []
        nrow = 0
        rows = questions_sheet.rows

        for row in rows:
            if nrow < 1:
                nrow += 1
                continue

            question = {}
            # Comprobamos que hay contenido en todas las celdas obligatorias
            if row[0].value is None or row[1] is None or row[2] is None:
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
                0   REF
                1   ORDER
                2   TITLE
                3   SCOPES
            """

            question['ref'] = str(row[0].value)
            question['title'] = str(row[1].value)
            if row[2].value is not None:
                question['scopes'] = str(
                    row[2].value).replace(' ', '').split(',')
            else:
                messages.add_message(
                    self.request,
                    messages.ERROR,
                    (
                        _('En la fila %s no se han establecido alcances para la pregunta') % str(
                            nrow+1)
                    )
                )
                return super(
                    GaQuestionnaireImport,
                    self
                ).form_invalid(form)
                break

            # Tenemos que comprobar que los alcances introducidos existen o se van a crear
            for scope in question['scopes']:
                if Scope.objects.filter(ref=scope).count() == 0:
                    # Si no existe previamente comprobamos que se va a crear en la importación
                    if scope not in [scope['ref'] for scope in scopes_to_create]:
                        messages.add_message(
                            self.request,
                            messages.ERROR,
                            (
                                _('En la fila %s el alcance %s no existe y no se va a crear en la importación') % (
                                    str(nrow+1), scope)
                            )
                        )
                        return super(
                            GaQuestionnaireImport,
                            self
                        ).form_invalid(form)
                        break

            nrow += 1
            questions_to_create.append(question)

        questionnaires_created = 0
        for q in questionnaires_to_create:
            if Questionnaire.objects.filter(ref=q['ref']).count() == 0:
                Questionnaire.objects.create(**q)
                questionnaires_created += 1

        scopes_created = 0
        for s in scopes_to_create:
            questionnaire = Questionnaire.objects.get(
                ref=s['questionnaire_ref'])
            if Scope.objects.filter(ref=s['ref']).count() == 0:
                scope = Scope.objects.create(
                    ref=s['ref'],
                    name=s['name'],
                    questionnaire=questionnaire
                )
                scopes_created += 1

            else:
                scope = Scope.objects.get(ref=s['ref'])

            if s['users'] is not None:
                for user_email in s['users']:
                    scope.user_to_assign.add(
                        User.objects.get(email=user_email))

        questions_created = 0
        for q in questions_to_create:
            if Question.objects.filter(ref=q['ref']).count() == 0:
                question = Question.objects.create(
                    ref=q['ref'],
                    title=q['title'],
                )
                questions_created += 1
            else:
                question = Question.objects.filter(ref=q['ref']).first()

            if q['scopes'] is not None:
                for scope in q['scopes']:
                    scope_object = Scope.objects.get(ref=scope)
                    if scope_object not in question.scopes.all():
                        question.scopes.add(scope_object)

        messages.add_message(
            self.request,
            messages.SUCCESS,
            (_(f"Cuestionario {questionnaire.name} importado correctamente con con {scopes_created} alcances y  {questions_created} preguntas")),
        )

        return super(GaQuestionnaireImport, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy("questionnaires:ga_questionnaire_list")
