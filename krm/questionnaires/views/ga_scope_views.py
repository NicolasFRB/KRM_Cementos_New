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
    ScopeCreateForm,
    ScopeUpdateForm
)
from krm.users.models import User

from krm.questionnaires.models import (
    Scope,
)

from krm.users.decorators import is_global_admin


@method_decorator([is_global_admin, ], name='dispatch')
class GaScopeDetailView(DetailView):
    model = Scope
    template_name = 'scopes/GaScopeDetail.html'
    context_object_name = 'scope'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            {'title': _('Alcances'), 'url': '#'},
            {'title': self.object.name}
        ]
        context['page_title'] = f"{_('Alcance')} : {self.object.name}"
        context['breadcrums'] = breadcrums
        context['js_template'] = ['js/custom/datatables.js']
        return context


@method_decorator([is_global_admin, ], name='dispatch')
class GaScopeCreateView(CreateView):
    form_class = ScopeCreateForm
    model = Scope
    template_name = 'scopes/GaScopeCreate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            {'title': _('Alcances'), 'url': '#'},
            #{'title': _('Nuevo Alcance'), 'url': reverse(
            #    'scopes:ga_scope_create')},
        ]
        context['page_title'] = _('Nuevo Alcance')
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
class GaScopeUpdateView(UpdateView):
    form_class = ScopeUpdateForm
    model = Scope
    template_name = 'scopes/GaScopeUpdate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            {'title': _('Cuestionario'), 'url': reverse(
                'questionnaires:ga_questionnaire_detail', kwargs={'pk': self.object.questionnaire.pk})},
            {'title': _('Editar alcance'), 'url': reverse(
                'scopes:ga_scope_detail', kwargs={'pk': self.object.pk})},
            {'title': _('Editar')},
        ]
        context['page_title'] = _('Editar Alcance')
        context['breadcrums'] = breadcrums
        return context

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Alcance actualizado correctamente')
        )
        return reverse_lazy(
            'scopes:ga_scope_detail',
            kwargs={'pk': self.object.pk}
        )


@method_decorator([is_global_admin, ], name='dispatch')
class GaScopeDeleteView(DeleteView):
    model = Scope
    template_name = "_includes/_base_confirm_delete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Cuestionarios'), 'url': reverse(
                'questionnaires:ga_questionnaire_list')},
            #{'title': _('Alcance'), 'url': reverse(
            #    'scopes:ga_scope_detail')},
            {'title': _('Eliminar')},
        ]
        context['page_title'] = _("Eliminar Alcance")
        context['breadcrums'] = breadcrums

        return context

    def get_success_url(self):
        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Alcance eliminado correctamente")
        )
        return reverse_lazy("questionnaires:ga_questionnaire_detail", kwargs={'pk': self.object.questionnaire.pk})

    def get_confirm_text_message(self):
        return _(
            '<span class="kt-font-bold">¿Seguro que desea eliminar el alcance y todas las preguntas asociadas?: </span> {0}? <span class="kt-font-bold">Se borrarán todos los datos asociados al mismo.</span>'
        ).format(str(self.object))
