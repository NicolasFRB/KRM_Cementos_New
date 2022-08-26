# -*- encoding: utf-8 -*-

from django.utils.decorators import method_decorator
from functools import wraps
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404

from krm.users.models import User
# from krm.manuscripts.models import Manuscript


class is_global_admin(object):

    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)

    def __call__(self, request, *args, **kwargs):
        response = self.view_func(request, *args, **kwargs)
        if request.user and request.user.is_superuser:
            return response
        raise PermissionDenied


class in_kpmg_group(object):

    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)

    def __call__(self, request, *args, **kwargs):
        response = self.view_func(request, *args, **kwargs)
        if request.user and request.user.groups.filter(name='Kpmg').exists():
            return response
        raise PermissionDenied

# def user_can_view_manuscript(function):
#     def wrap(request, *args, **kwargs):
#         try:
#             p = Manuscript.objects.get(pk=kwargs["pk"])
#         except Manuscript.DoesNotExist:
#             raise Http404

#         if request.user.is_superuser:
#             return function(request, *args, **kwargs)

#         # Si su grupo empresarial tiene derecho a usar el proceso
#         if p.office in [office for office in request.user.offices.all()]:
#             return function(request, *args, **kwargs)

#         raise PermissionDenied

#     return wrap
