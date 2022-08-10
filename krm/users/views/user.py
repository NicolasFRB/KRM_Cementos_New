import requests

# Django
from django.urls import reverse_lazy, reverse
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from django.contrib import messages
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
    FormView,
    TemplateView
)

from krm.metronic.__init__ import KTLayout
from krm.metronic.libs.theme import KTTheme

from krm.users.models import User

from krm.users.forms import(
    UserCreateForm,
)

from krm.users.decorators import (
    is_global_admin,
)


@method_decorator([login_required, is_global_admin], name='dispatch')
class UserList(ListView):
    template_name = 'users/UserList.html'
    model = User
    context_object_name = 'users'


@method_decorator([login_required, is_global_admin], name='dispatch')
class UserDetail(DetailView):
    template_name = 'users/UserDetail.html'
    model = User


@method_decorator([login_required, is_global_admin], name='dispatch')
class UserCreate(CreateView):
    template_name = 'users/UserCreate.html'
    model = User
    form_class = UserCreateForm

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario añadido correctamente')
        )
        return reverse_lazy(
            'users:user_list'
        )


@method_decorator((login_required, is_global_admin), name='dispatch')
class UserUpdate(UpdateView):
    template_name = 'users/UserUpdate.html'
    model = User
    form_class = UserCreateForm

    def get_context_data(self, **kwargs):
        context = super(UserUpdate, self).get_context_data(**kwargs)
        context['title_template'] = _('Editar usuario')
        return context

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario modificado correctamente')
        )

        return reverse_lazy(
            'users:user_list'
        )


@method_decorator((login_required, is_global_admin), name='dispatch')
class UserDelete(DeleteView):
    model = User
    template_name = '_layout/_base_confirm_delete.html'

    def get_title_template(self):
        return u'Eliminar Usuario: %s' % self.object.email

    def get_confirm_text_message(self):
        return _('¿Seguro que desea <span class="kt-font-bold">eliminar el Usuario %s</span>? Se borrarán todos los datos asociados al mismo.') % self.object.email

    def get_success_url(self):
        messages.add_message(
            self.request,
            messages.SUCCESS,
            _('Usuario eliminado correctamente')
        )

        return reverse_lazy(
            'users:user_list'
        )


@method_decorator((login_required, is_global_admin), name='dispatch')
class TestView(TemplateView):
    template_name = 'pages/Pruebas.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        # url = "https://sage200.sage.es/api/sales/Products?api-version=1.0&$filter=CompanyId eq 'c68f8957-e914-42a4-ac9f-e36c1bb026e8'"
        url = "https://sage200.sage.es/api/sales/Products?api-version=1.0"

        payload = {}
        headers = {
            'X-Nonce': '2',
            'X-Site': '9f098e6a-1566-4b0e-ab6b-d2692313337e',
            'Ocp-Apim-Subscription-Key': 'wg6Ew/XnDxTdH2hkp69SchF1hN5p/owuKRzU0t0bsnU=',
            'Accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56TXdPVVJHTVVZNU5ERXpRelJHUVVNMVF6azJSa1U1UVRJMU0wRTROemhGUmpWQ04wSTNOQSJ9.eyJpc3MiOiJodHRwczovL2lkLnNhZ2UuY29tLyIsInN1YiI6ImF1dGgwfDdhZDI2ZTI0MDY3NzRhNWM3ZDMxMjZmNjAwYzM4ODlmMDAwYWM5MjcxZmUyZGNjMyIsImF1ZCI6InMyZXNwL3MyMDAuc2FnZS5jb20vYXBpIiwiaWF0IjoxNjU3NjkzMTk4LCJleHAiOjE2NTc3MjE5OTgsImF6cCI6ImphcklMUmVXdm92RWVnTEZVUzUxTHNrUU45cUxweTcyIiwic2NvcGUiOiJvZmZsaW5lX2FjY2VzcyJ9.bCWih9_68--BRkn4U1KAO327XmN1DgF0jiI_R9_TB9pD9gtaTNWMnx9ZdsFv5hrW4tdkNhYM85XZ7FAjw1ABiYOcSvKuwkQNO0uZBg1JT_DzcMXC0MKFR269bs2eVCDGeLrnQmoKPzudNu_O1MMFdQZuwTPD7ceQFZd3bm54xBg_XZ4qYVPXashm0oeW6RpIbh0mW5yDAWO1umb3VXoOK0vHcW0N_0qx8YCJ2KbaOdyXwZJ2yAk99bTh55wvWZEpbCSp9791T2bwJVUfLBWGAsx_jHUy01P0EqCsfmk4dvRvL5Tb96zQ5DhsyVLKymZD0q2B1rAZtBEVx0r855LikQ',
            'Cookie': '__cf_bm=GcPj40uC6dDHMi3Nt13uzWbRgg8qmG6BqywxKoVvZgc-1657561279-0-ASgEfFOXQIdywIVi6SxNT6dBceSNX6R+BcpJ882UDTMbg2J4GqE50HzibitMfgkMNRQzgiINRuuwiiY9BE7wRtk='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        print(response.text)
        # import ipdb
        # ipdb.set_trace()
        context['data'] = response.text

        return context


@method_decorator((login_required, is_global_admin), name='dispatch')
class SageStatus(TemplateView):
    template_name = 'sage/SageStatus.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        # url = "https://sage200.sage.es/api/sales/Products?api-version=1.0&$filter=CompanyId eq 'c68f8957-e914-42a4-ac9f-e36c1bb026e8'"
        url = "https://sage200.sage.es/api/sales/Products?api-version=1.0"

        payload = {}
        headers = {
            'X-Nonce': '2',
            'X-Site': '9f098e6a-1566-4b0e-ab6b-d2692313337e',
            'Ocp-Apim-Subscription-Key': 'wg6Ew/XnDxTdH2hkp69SchF1hN5p/owuKRzU0t0bsnU=',
            'Accept': 'application/json',
            'Authorization': 'Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik56TXdPVVJHTVVZNU5ERXpRelJHUVVNMVF6azJSa1U1UVRJMU0wRTROemhGUmpWQ04wSTNOQSJ9.eyJpc3MiOiJodHRwczovL2lkLnNhZ2UuY29tLyIsInN1YiI6ImF1dGgwfDdhZDI2ZTI0MDY3NzRhNWM3ZDMxMjZmNjAwYzM4ODlmMDAwYWM5MjcxZmUyZGNjMyIsImF1ZCI6InMyZXNwL3MyMDAuc2FnZS5jb20vYXBpIiwiaWF0IjoxNjU3NjkzMTk4LCJleHAiOjE2NTc3MjE5OTgsImF6cCI6ImphcklMUmVXdm92RWVnTEZVUzUxTHNrUU45cUxweTcyIiwic2NvcGUiOiJvZmZsaW5lX2FjY2VzcyJ9.bCWih9_68--BRkn4U1KAO327XmN1DgF0jiI_R9_TB9pD9gtaTNWMnx9ZdsFv5hrW4tdkNhYM85XZ7FAjw1ABiYOcSvKuwkQNO0uZBg1JT_DzcMXC0MKFR269bs2eVCDGeLrnQmoKPzudNu_O1MMFdQZuwTPD7ceQFZd3bm54xBg_XZ4qYVPXashm0oeW6RpIbh0mW5yDAWO1umb3VXoOK0vHcW0N_0qx8YCJ2KbaOdyXwZJ2yAk99bTh55wvWZEpbCSp9791T2bwJVUfLBWGAsx_jHUy01P0EqCsfmk4dvRvL5Tb96zQ5DhsyVLKymZD0q2B1rAZtBEVx0r855LikQ',
            'Cookie': '__cf_bm=GcPj40uC6dDHMi3Nt13uzWbRgg8qmG6BqywxKoVvZgc-1657561279-0-ASgEfFOXQIdywIVi6SxNT6dBceSNX6R+BcpJ882UDTMbg2J4GqE50HzibitMfgkMNRQzgiINRuuwiiY9BE7wRtk='
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        return context
