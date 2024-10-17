
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
from krm.evaluations.forms.evaluation_forms import EvaluationAssignImportForm, EvaluationDownload, EvaluationActionForm, EvaluationTemplateAssignDownload
from krm.evaluations.models.control_test_model import ControlTest

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.evaluations.forms import (
    ControlTestAssignForm,
    ControlTestAnswerSupervisorCreateForm,
    ControlTestAnswerOwnerCreateForm,
)

from krm.evaluations.models import Evaluation, ControlTestAnswer
from krm.companies.models import Company
from krm.controls.models import Control
from krm.users.models import User

from krm.evaluations.forms import ControlTestUpdateForm, ControlTestCaForm


from krm.users.decorators import (
    is_global_admin,
    user_can_assign_control_test,
    user_can_view_control_test,
    is_company_admin
)


@method_decorator([login_required, user_can_assign_control_test], name="dispatch")
class CaControlTestAssign(UpdateView, is_company_admin):
    form_class = ControlTestAssignForm
    model = ControlTest
    template_name = "control_tests/ga/ControlTestAssign.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Evaluación'), 'url': reverse(
                'evaluations:ca_evaluation_detail', kwargs={'pk': self.object.evaluation.pk})},
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
            "evaluations:ca_evaluation_detail",
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


@method_decorator([login_required, is_company_admin], name="dispatch")
class CaControlTestAdministratorList(TemplateView):
    template_name = "control_tests/ca/CaControlTestAdministratorList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Control Test para administrar'), 'url': reverse(
                'control_tests:ca_control_test_administrator_list')}
        ]
        context['page_title'] = _('Control Tests para administrar')
        context['breadcrums'] = breadcrums

        context["control_test_administrator"] = self.request.user.controls_test_administrator_pending()
        context["control_test_finished"] = self.request.user.controls_test_administrator_finished()
        context['js_template'] = ['js/custom/datatables.js']

        return context


@method_decorator((login_required, user_can_view_control_test), name="dispatch")
class CaControlTestDetail(FormView):
    template_name = 'control_tests/ca/CaControlTestDetail.html'
    form_class = ControlTestCaForm

    def dispatch(self, request, *args, **kwargs):
        control_test = get_object_or_404(ControlTest, pk=self.kwargs.get("pk"))
        self.control_test = control_test
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        from datetime import date
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Control Test')}
        ]
        context['page_title'] = f"{_('Control Test')} : {self.control_test.identifier}"
        context['breadcrums'] = breadcrums
        context['control_test'] = self.control_test
        context['control'] = self.control_test.control
        context['control_test_risks_company'] = self.control_test.get_control_test_risks_company()
        context['control_test_subprocess'] = self.control_test.get_control_test_subprocess()
        return context

    def form_valid(self, form):
        if form.cleaned_data["control_status"] == self.control_test.status:
            messages.add_message(
                self.request,
                messages.ERROR,
                _('Debe establecer un nuevo estado del control para finalizar la revisión del control test')
            )
            return super(
                CaControlTestDetail,
                self
            ).form_invalid(form)

        if form.cleaned_data["control_status"] == 'RE':
            self.control_test.status = 'WO'
            self.control_test.result = 'SE'
            self.control_test.answers.all().delete()
        else:
            self.control_test.status = form.cleaned_data["control_status"]
            self.control_test.result = form.cleaned_data["control_result"]

        # Apuntamos en el diario del usuario la acción
        self.request.user.add_action(
            "Control Test Compl.: %s" % str(self.control_test.identifier)
        )

        # Ahora para mandar las notificaciones comprobamos a quien corresponde
        self.control_test.save()
        self.control_test.send_notification('Notification')

        description = form.cleaned_data["description"]
        if description:
            ControlTestAnswer.objects.create(
                control_test=self.control_test,
                description=description,
                user=self.request.user,
            )

        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Control administrado correctamente")
        )

        return reverse_lazy(
            "control_tests:ca_control_test_administrator_list"
        )

    def get_initial(self):
        return {
            'control_status': self.control_test.status,
            'control_result': self.control_test.result
        }
