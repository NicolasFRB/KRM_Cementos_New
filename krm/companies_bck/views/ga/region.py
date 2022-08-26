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
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.shortcuts import get_object_or_404

from django.views.generic import (
    FormView,
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from django.contrib.auth.decorators import login_required

from krc.business_group.models import (
    BusinessGroup,
    Company
)

# from krc.business_group.forms import (
#     RegionCreateForm
# )

decorators = [
    csrf_protect,
    never_cache,
]


# @method_decorator(login_required, name='dispatch')
# class RegionList(ListView):
#     template_name = 'region/ga/RegionList.html'
#     model = Region

# @method_decorator(login_required, name='dispatch')
# class RegionCreate(CreateView):
#     form_class = RegionCreateForm
#     model = Region
#     template_name = 'region/ga/RegionCreate.html'

#     def get_initial(self):
#         business_group = get_object_or_404(BusinessGroup, pk=self.kwargs.get('pk'))
#         return {
#             'business_group' : business_group
#         }
#     def get_context_data(self, **kwargs):
#         context = super(RegionCreate, self).get_context_data(**kwargs)
#         context['business_group'] = get_object_or_404(BusinessGroup, pk=self.kwargs.get('pk'))
#         context['title_template'] = _('Nueva Región')
#         return context

#     def get_success_url(self):
#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             _('Región creada correctamente')
#         )
#         return reverse_lazy(
#             'business_group:ga_region_detail',
#             kwargs={'pk': self.object.pk}
#         )

# @method_decorator(login_required, name='dispatch')
# class RegionUpdate(UpdateView):
#     form_class = RegionCreateForm
#     model = Region
#     template_name = 'region/ga/RegionCreate.html'

#     def get_context_data(self, **kwargs):
#         context = super(RegionUpdate, self).get_context_data(**kwargs)
#         context['business_group'] = self.object.business_group
#         context['title_template'] = _('Editar Región')
#         return context

#     def get_success_url(self):
#         messages.add_message(
#             self.request,
#             messages.SUCCESS,
#             _('Región modificacda correctamente')
#         )
#         return reverse_lazy(
#             'business_group:ga_region_detail',
#             kwargs={'pk': self.object.pk}
#         )

# @method_decorator(login_required, name='dispatch')
# class RegionDelete(DeleteView):
#     model = Region
#     template_name = 'layout/_base_confirm_delete.html'

#     def get_success_url(self):
#         messages.add_message(
#             self.request, messages.SUCCESS,
#             _('Región eliminada correctamente')
#         )
#         return reverse_lazy(
#             'business_group:ga_business_group_detail',
#             kwargs={'pk': self.object.business_group.pk}
#         )

#     def get_title_template(self):
#         return u'Eliminar Región: %s' % self.object.name

#     def get_confirm_text_message(self):
#         return _('¿Seguro que desea <span class="kt-font-bold">eliminar la Región %s</span>? Se borrarán todos los datos asociados a la misma.') % self.object.name

# @method_decorator(login_required, name='dispatch')
# class RegionDetail(DetailView):
#     template_name = 'region/ga/RegionDetail.html'
#     model = Region


#     def get_context_data(self, **kwargs):
#         context = super(RegionDetail, self).get_context_data(**kwargs)
#         region = get_object_or_404(Region, pk=self.kwargs.get('pk'))
#         context['bg'] = region.business_group
#         if 'tab' in self.kwargs:
#             context['active'] =  self.kwargs.get('tab')
#         else:
#             context['active'] =  'tab-dashboard'

#         if context['active'] == 'tab-dashboard':
#             context['process_tests_status'] = self.object.get_process_tests_status_aggregate()
#             context['control_tests_status'] = self.object.get_control_tests_status_aggregate()
#             context['control_tests_result'] = self.object.get_control_tests_result_aggregate()
#         return context
