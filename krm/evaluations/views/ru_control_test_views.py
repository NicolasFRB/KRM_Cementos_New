
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
    ControlTestAnswerCreateForm,
    ControlTestAnswerSupervisorCreateForm,
    ControlTestAnswerOwnerCreateForm,
    RemediationPlanCreateForm,
    ControlTestCaForm
)

from krm.users.decorators import (
    is_global_admin,
    user_can_assign_control_test,
    user_can_view_control_test
)

from krm.evaluations.models import (
    ControlTest,
    ControlTestAnswer,
    RemediationPlan
)


@method_decorator((login_required, user_can_view_control_test), name="dispatch")
class RuControlTestDetail(CreateView):
    template_name = 'control_tests/ga/ControlTestDetail.html'
    model = ControlTestAnswer

    def dispatch(self, request, *args, **kwargs):
        control_test = get_object_or_404(ControlTest, pk=self.kwargs.get("pk"))
        self.control_test = control_test

        if control_test.remediation_plan_needed and self.request.user == control_test.control_test_owner:
            return HttpResponseRedirect(reverse("control_tests:ru_control_test_detail_create_remediation_plan", kwargs={"pk": control_test.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_form_class(self):
        if (
            self.request.user == self.control_test.control_test_owner
            and self.control_test.status == "WO"
        ):
            return ControlTestAnswerOwnerCreateForm
        elif (
            self.request.user == self.control_test.control_test_supervisor
            and self.control_test.status == "WS"
        ):
            return ControlTestAnswerSupervisorCreateForm
        elif self.control_test.evaluation.company in self.request.user.companies_admin.all():
            return ControlTestCaForm
        else:
            return ControlTestAnswerCreateForm

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
        if self.control_test.evaluation.company in self.request.user.companies_admin.all():
            context['ca'] = True
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.control_test = self.control_test
        self.answer = form.save()

        # Ha respondido el control test owner
        if isinstance(form, ControlTestAnswerOwnerCreateForm):
            control_result = form.cleaned_data["control_result"]

            self.control_test.result = control_result
            if self.control_test.result == "NE":
                self.control_test.status = "WO"
                self.control_test.remediation_plan_needed = True
            else:
                self.control_test.status = "WS"

        # Ha respondido el control supervisor
        elif isinstance(form, ControlTestAnswerSupervisorCreateForm):
            if "more_information" in form.cleaned_data:
                if form.cleaned_data["more_information"] == True:
                    self.control_test.status = "WO"
                    self.control_test.result = "SE"
                else:
                    self.control_test.status = "WA"

        # Ha respondido el control administrator
        elif isinstance(form, ControlTestCaForm):
            self.control_test.status = form.cleaned_data["status"]
            self.control_test.result = form.cleaned_data["result"]

        # Apuntamos en el diario del usuario la acción
        self.request.user.add_action(
            "Control Test Compl.: %s" % str(self.control_test.identifier)
        )

        # Ahora para mandar las notificaciones comprobamos a quien corresponde
        self.control_test.save()
        self.control_test.send_notification()

        return super().form_valid(form)

    def get_success_url(self):

        if self.request.user == self.control_test.control_test_owner:

            if self.control_test.result == "EF":
                messages.add_message(
                    self.request,
                    messages.SUCCESS,
                    _("Control completado correctamente"),
                )

                return reverse_lazy("control_tests:ru_control_test_owner_list")

            else:
                if self.control_test.status == "WO":
                    return reverse_lazy(
                        "control_tests:ru_control_test_detail",
                        kwargs={"pk": self.control_test.pk},
                    )
                else:
                    messages.add_message(
                        self.request,
                        messages.SUCCESS,
                        _("Control completado correctamente"),
                    )

                    return reverse_lazy("control_tests:ru_control_test_owner_list")

        if self.request.user == self.control_test.control_test_supervisor:
            messages.add_message(
                self.request, messages.SUCCESS, _(
                    "Control revisado correctamente")
            )
            return reverse_lazy("control_tests:ru_control_test_supervisor_list")

        # Si es efectivo se retorna a la tabla de controles por rellenar

        messages.add_message(
            self.request, messages.SUCCESS, _(
                "Control completado correctamente")
        )

        return reverse_lazy(
            "evaluations:ga_evaluation_detail",
            kwargs={"pk": self.control_test.pk},
        )

    def get_initial(self):
        control_test = ControlTest.objects.get(pk=self.kwargs.get("pk"))
        return {
            'status': control_test.status,
            'result': control_test.result
        }


@method_decorator((login_required, user_can_view_control_test), name="dispatch")
class RuRemediationPlanCreate(CreateView):
    template_name = 'control_tests/ga/ControlTestDetail.html'
    model = RemediationPlan
    form_class = RemediationPlanCreateForm

    def dispatch(self, request, *args, **kwargs):
        control_test = get_object_or_404(ControlTest, pk=self.kwargs.get("pk"))
        self.control_test = control_test

        if not control_test.remediation_plan_needed:
            return HttpResponseRedirect(reverse("control_tests:ru_control_test_detail", kwargs={"pk": control_test.pk}))
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        from datetime import date
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)

        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Control Test')},
            {'title': _('Nuevo Plan de Remediación')},
        ]
        context['page_title'] = f"{_('Nuevo Plan de Remediación para el Control Test')} : {self.control_test.identifier}"
        context['breadcrums'] = breadcrums
        context['control_test'] = self.control_test
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.control_test = self.control_test
        self.remediation_plan = form.save()

        self.control_test.status = 'WS'
        self.control_test.remediation_plan_needed = False

        # Apuntamos en el diario del usuario la acción
        self.request.user.add_action(
            "Plan de Remediación establecido para el Control Test: %s" % str(
                self.control_test.identifier)
        )

        # Ahora para mandar las notificaciones comprobamos a quien corresponde
        self.control_test.save()
        self.control_test.send_notification()

        return super().form_valid(form)

    def get_success_url(self):

        messages.add_message(
            self.request,
            messages.SUCCESS,
            _("Plan de remediación establecido correctamente"),
        )

        return reverse_lazy("control_tests:ru_control_test_owner_list")


@method_decorator(login_required, name="dispatch")
class RuControlTestOwnerList(TemplateView):
    template_name = "control_tests/ru/RuControlTestOwnerList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Control Test para supervisar'), 'url': reverse(
                'control_tests:ru_control_test_supervisor_list')}
        ]
        context['page_title'] = _('Control Tests asignados como Control Owner')
        context['breadcrums'] = breadcrums

        context["control_test_pending"] = self.request.user.controls_test_owner.filter(
            status="WO"
        )
        context["control_test_revision"] = self.request.user.controls_test_owner.filter(
            status="WS"
        )
        context["control_test_administrator"] = self.request.user.controls_test_owner.filter(
            status="WA"
        )
        context["control_test_finished"] = self.request.user.controls_test_owner.filter(
            status="FI"
        )
        context['js_template'] = ['js/custom/datatables.js']

        return context


@method_decorator(login_required, name="dispatch")
class RuControlTestSupervisorList(TemplateView):
    template_name = "control_tests/ru/RuControlTestSupervisorList.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        breadcrums = [
            {'title': _('Dashboard'), 'url': reverse('users:dashboard')},
            {'title': _('Control Test para supervisar'), 'url': reverse(
                'control_tests:ru_control_test_supervisor_list')}
        ]
        context['page_title'] = _(
            'Control Test asignados como Control supervisor')
        context['breadcrums'] = breadcrums

        context["control_test_pending"] = self.request.user.controls_test_supervisor.filter(
            status="WS"
        )
        context["control_test_revision"] = self.request.user.controls_test_supervisor.filter(
            status="WO"
        )
        context["control_test_administrator"] = self.request.user.controls_test_owner.filter(
            status="WA"
        )
        context["control_test_finished"] = self.request.user.controls_test_supervisor.filter(
            status="FI"
        )
        context['js_template'] = ['js/custom/datatables.js']

        return context
