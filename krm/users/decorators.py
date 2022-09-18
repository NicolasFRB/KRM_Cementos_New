# -*- encoding: utf-8 -*-

from django.utils.decorators import method_decorator
from functools import wraps
from django.urls import reverse_lazy
from django.shortcuts import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.http import Http404

from krm.users.models import User
from krm.evaluations.models import Evaluation
from krm.evaluations.models import ControlTest


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


class is_company_admin(object):

    def __init__(self, view_func):
        self.view_func = view_func
        wraps(view_func)(self)

    def __call__(self, request, *args, **kwargs):
        response = self.view_func(request, *args, **kwargs)
        if request.user.is_company_admin:
            return response
        raise PermissionDenied


def user_can_assign_control_test(function):
    def wrap(request, *args, **kwargs):
        try:
            ct = ControlTest.objects.get(pk=kwargs["pk"])
        except ControlTest.DoesNotExist:
            raise Http404

        if request.user.is_superuser:
            return function(request, *args, **kwargs)

        if ct.evaluation.company in request.user.companies_admin.all():
            return function(request, *args, **kwargs)

        raise PermissionDenied

    return wrap


def user_can_view_control_test(function):
    def wrap(request, *args, **kwargs):
        try:
            ct = ControlTest.objects.get(pk=kwargs["pk"])
        except ControlTest.DoesNotExist:
            raise Http404

        if (
            request.user.is_superuser
            or request.user == ct.control_test_supervisor
            or request.user == ct.control_test_owner
            or ct.evaluation.company in request.user.companies_admin.all()
        ):
            return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap


def user_can_view_evaluation(function):
    def wrap(request, *args, **kwargs):
        try:
            evaluation = Evaluation.objects.get(pk=kwargs["pk"])
        except Evaluation.DoesNotExist:
            raise Http404

        if (
            evaluation.company in request.user.companies_admin.all()
        ):
            return function(request, *args, **kwargs)
        raise PermissionDenied

    return wrap
