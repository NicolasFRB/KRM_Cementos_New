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
