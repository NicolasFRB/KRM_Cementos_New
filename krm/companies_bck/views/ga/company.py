# -*- encoding: utf-8 -*-
"""Users views."""

# Django
from django.contrib.auth import login, authenticate, logout
from datetime import date
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.shortcuts import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    CreateView,
    DetailView
)

from django.contrib.auth.decorators import login_required

from krc.business_group.models import (
    BusinessGroup,
    Company
)

from krc.process.models import (
    Control,
    Process
)

from krc.process_test.models import (
    ControlTest,
    ControlTestAnswer,
    ProcessTest
)

from krc.users.models import User

from krc.business_group.forms import (
    CompanyCreateForm
)

from krc.utils import COLORS


# @method_decorator(login_required, name='dispatch')
# class CompanyList(ListView):
#     template_name = 'company/ga/CompanyList.html'
#     model = Company


# @method_decorator(login_required, name='dispatch')
# class CompanyDetail(DetailView):
#     template_name = 'company/ga/CompanyDetail.html'
#     model = Company

#     def get_context_data(self, **kwargs):
#         context = super(CompanyDetail, self).get_context_data(**kwargs)
#         # context['region'] =  self.object.region

#         # from django.db.models import Count
#         # controls = ControlTest.objects.filter(process_test__in=self.object.process_tests.all()).values('status').annotate(num_controls=Count('id'))

#         # gd_controls = []
#         # for c in controls:
#         #     e = {}
#         #     e['label'] = COLORS[c['status']]['label']
#         #     e['color'] = COLORS[c['status']]['color']
#         #     e['data'] = c['num_controls']
#         #     gd_controls.append(e)
#         # context['gd_controls'] =  gd_controls

#         # process = self.object.process_tests.all().values('status').annotate(num_controls=Count('id'))
#         # gd_process = []
#         # for c in process:
#         #     e = {}
#         #     e['label'] = COLORS[c['status']]['label']
#         #     e['color'] = COLORS[c['status']]['color']
#         #     e['data'] = c['num_controls']
#         #     gd_process.append(e)
#         # context['gd_process'] =  gd_process

#         context['process_tests_status'] = self.object.get_process_tests_status_aggregate()
#         context['control_tests_status'] = self.object.get_control_tests_status_aggregate()
#         context['control_tests_result'] = self.object.get_control_tests_result_aggregate()

#         return context


# @method_decorator(login_required, name='dispatch')
# class CompanyCreate(CreateView):
#     form_class = CompanyCreateForm
#     model = Company
#     template_name = 'company/ga/CompanyCreate.html'

#     # def get_initial(self):
#     #     region = get_object_or_404(Region, pk=self.kwargs.get('pk'))
#     #     return {
#     #         'region' : region
#     #     }
#     # def get_context_data(self, **kwargs):
#     #     context = super(CompanyCreate, self).get_context_data(**kwargs)
#     #     context['region'] =  get_object_or_404(Region, pk=self.kwargs.get('pk'))
#     #     return context

# def get_success_url(self):
#     messages.add_message(
#         self.request,
#         messages.SUCCESS,
#         _('Compañía añadida correctamente')
#     )
#     return reverse_lazy(
#         'business_group:ga_region_detail',
#         kwargs={'pk': self.object.region.pk}
#     )
