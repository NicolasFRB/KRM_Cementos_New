
from django.shortcuts import render

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

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationInitForm, EvaluationTemplateAssignDownload
from krm.evaluations.models.control_test_model import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.forms import (
    ControlTestAssignForm,
    ControlTestAnswerSupervisorCreateForm,
    ControlTestAnswerOwnerCreateForm,
)

from krm.evaluations.models import Evaluation
from krm.companies.models import Company
from krm.controls.models import Control
from krm.users.models import User

from krm.evaluations.forms import ControlTestUpdateForm


from krm.users.decorators import (
    is_global_admin,
    user_can_assign_control_test,
    user_can_view_control_test
)


@method_decorator([login_required, user_can_assign_control_test], name="dispatch")
class ControlTestAssign(UpdateView):
    form_class = ControlTestAssignForm
    model = ControlTest
    template_name = "control_tests/ga/ControlTestAssign.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluación'), 'url': reverse(
                'evaluations:ga_evaluation_detail', kwargs={'pk': self.object.evaluation.pk})},
            {'title': self.object.identifier}
        ]
        context['page_title'] = f"{_('Control Test')} : {self.object.identifier}"
        context['breadcrums'] = breadcrums
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Test de Control asignado correctamente"),
        )
        return reverse_lazy(
            "evaluations:ga_evaluation_detail",
            kwargs={"pk": self.object.evaluation.pk},
        )

    def get_form(self, form_class=None):
        form_class = super().get_form(form_class=None)
        users = User.objects.filter(
            companies__in=(self.object.evaluation.company,),
            is_active=True
        )
        form_class.fields["control_test_supervisor"].queryset = users
        form_class.fields["control_test_owner"].queryset = users
        return form_class


@method_decorator((login_required, user_can_view_control_test), name="dispatch")
class ControlTestDetail(DetailView):
    model = ControlTest
    context_object_name = 'control_test'
    template_name = "control_tests/ga/ControlTestDetail.html"

    # def dispatch(self, request, *args, **kwargs):
    #     if self.get_object().evaluation.company in request.user.companies_admin.all():
    #         return HttpResponseRedirect(reverse_lazy(
    #             "control_tests:ca_control_test_detail",
    #             kwargs={'pk': self.get_object().pk}
    #         ))
    #     return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluación'), 'url': reverse(
                'evaluations:ga_evaluation_detail', kwargs={'pk': self.object.evaluation.pk})},
            {'title': self.object.identifier}
        ]
        context['page_title'] = f"{_('Control Test')} : {self.object.identifier}"
        context['breadcrums'] = breadcrums

        if self.object.evaluation.company in self.request.user.companies_admin.all():
            context['is_company_admin'] = True

        return context


@method_decorator((login_required, user_can_view_control_test), name="dispatch")
class ControlTestUpdate(UpdateView):
    model = ControlTest
    context_object_name = 'control_test'
    template_name = "control_tests/ga/ControlTestUpdate.html"
    form_class = ControlTestUpdateForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluación'), 'url': reverse(
                'evaluations:ga_evaluation_detail', kwargs={'pk': self.object.evaluation.pk})},
            {'title': self.object.identifier}
        ]
        context['page_title'] = f"{_('Editar Control Test')} : {self.object.identifier}"
        context['breadcrums'] = breadcrums
        return context

    def form_valid(self, form):
        send_notification = form.cleaned_data["send_notification"]
        if send_notification:
            self.object.send_notification()
        return super().form_valid(form)

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Test de Control modificado correctamente"),
        )
        return reverse_lazy(
            "control_tests:control_test_detail",
            kwargs={"pk": self.object.pk},
        )
