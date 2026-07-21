from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory, TestCase
from django.contrib.auth.models import AnonymousUser
from django.urls import reverse_lazy, reverse
from django.test import Client

from krm.users.models import User
from krm.users.views import (
    LoginView,
    DashboardView
)

# from krm.users.tests import UserTestModel

from django.test import TestCase
from django.test import Client

# Model
from krm.users.models import User

# Form
from krm.users.forms import LoginForm

class BaseTest(TestCase):

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Test',
            last_name='Test',
            email='no-replay-krctool@gcpv.com',
            username='no-replay-krctool@gcpv.com',
            password=''
        )
        self.user.set_password('admin123')
        self.user.save()
        self.client = Client()


class LoginViewTest(BaseTest):

    def test_can_access_page(self):
        response = self.client.get(reverse('auth:login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/UsersLogin.html')

    def test_anonymous(self):
        req = RequestFactory().get(reverse("users:login"))
        req.user = AnonymousUser()
        resp = LoginView.as_view()(req)
        assert resp.status_code == 200

    def test_with_user_register(self):
        req = RequestFactory().get(reverse("users:login"))
        req.user = self.user
        resp = LoginView.as_view()(req)
        assert resp.status_code == 302, "Si está logueado, debe redireccionar"

    def test_login_form(self):
        resp = self.client.post(
            reverse('auth:login'), {
                'username': 'no-replay-krctool@gcpv.com',
                'password': '',
            }
        )
        assert resp.status_code == 302
        self.assertRedirects(resp, '/dashboard/')


class DashboardViewTest(BaseTest):

    def test_anonymous(self):
        resp = self.client.get(reverse('users:dashboard'))
        # self.assertTemplateUsed(resp, 'users/UserLogin.html')
        assert resp.status_code == 302
        self.assertRedirects(resp, '/login/?next=/dashboard/')

    def test_with_user_register(self):
        self.client.login(
            username='no-replay-krctool@gcpv.com',
            password='test'
        )
        resp = self.client.get(reverse('users:dashboard'))
        assert resp.context['user'] == self.user
        self.assertTemplateUsed(resp, 'users/Dashboard.html')
        assert resp.status_code == 200


    def test_form_valid_on_login_view(self):
        factory = RequestFactory()
        data = {
            'username': 'Billy',
            'password': 'Masters'
        }

        req = factory.post(reverse('auth:login'), data=data)
        req.user = AnonymousUser()

        req._dont_enforce_csrf_checks = True

        """Annotate a request object with a session"""
        middleware = SessionMiddleware()
        middleware.process_request(req)
        req.session.save()

        """Annotate a request object with a messages"""
        middleware = MessageMiddleware()
        middleware.process_request(req)
        req.session.save()

        # this will submit the form and run the form_valid.
        response = LoginView.as_view()(req)
        self.assertEqual(response.status_code, 200)

    def test_with_authenticated_client(self):
        username = "user1"
        password = "bar"
        user = User.objects.create_user(
            username=username, password=password)
        client = Client()
        # Use this:
        client.force_login(user)
        # Or this:
        client.login(username=username, password=password)
        response = client.get(reverse_lazy('users:dashboard'))
        # assert response.content == 'Protected Area'
        print(response.context['user'])
        self.assertEqual(response.status_code, 200)
