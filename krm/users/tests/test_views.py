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


# https://docs.python.org/3/library/http.html

# class UserTestModel(TestCase):

#     def setUp(self):
#         """Test case setup."""
#         self.user = User.objects.create(
#             first_name='Bienvenido',
#             last_name='Sáez Muelas',
#             email='bienvenidosaez@baetica.com',
#             username='bienvenidosaez@baetica.com',
#             password='admin123'
#         )


# class TestLoginView(UserTestModel):

#     def test_anonymous(self):
#         req = RequestFactory().get(reverse("users:login"))
#         req.user = AnonymousUser()
#         resp = LoginView.as_view()(req)
#         assert resp.status_code == 200

#     def test_with_user_register(self):
#         req = RequestFactory().get(reverse("users:login"))
#         req.user = self.user
#         resp = LoginView.as_view()(req)
#         assert resp.status_code == 302, "Si está logueado, debe redireccionar"

#     # def test_login_post(self):
#     #     data = {
#     #         "username": "bienvenidosaez@baetica.com",
#     #         "password": 'admin123'
#     #     }
#     #     form = LoginForm(data=data)
#     #     assert form.is_valid()
#     #     req = RequestFactory().post(
#     #         reverse("users:login"),
#     #         kwargs={},
#     #         data=form.data
#     #     )

#     #     req._dont_enforce_csrf_checks = True
#     #     req.user = AnonymousUser()

#     #     """Annotate a request object with a session"""
#     #     middleware = SessionMiddleware()
#     #     middleware.process_request(req)
#     #     req.session.save()

#     #     """Annotate a request object with a messages"""
#     #     middleware = MessageMiddleware()
#     #     middleware.process_request(req)
#     #     req.session.save()

#     #     resp = LoginView.as_view()(req)
#     #     assert resp.url == "/dashboard/"
#     #     assert resp.status_code == 302, "Should redirect to success url"

#     def test_login_post(self):
#         # send login data
#         data = {
#             "username": "bienvenidosaez@baetica.com",
#             "password": 'admin123'
#         }
#         resp = self.client.post(
#             reverse("users:login"), data, follow=True)

#         # should be logged in now
#         assert resp.status_code == 200
#         assert resp.context['user'].is_authenticated == True
#         assert resp.user.username == "bienvenidosaez@baetica.com"


# class BaseTest(TestCase):
#     def setUp(self):
#         self.login_url = reverse('auth:login')
#         self.correct_user_data = {
#             'first_name': 'Bienvenido',
#             'last_name': 'Sáez Muelas',
#             'email': 'testemail@gmail.com',
#             'username': 'testemail@gmail.com',
#             'password': 'password',
#             'password2': 'password',
#         }
#         # self.user_short_password = {
#         #     'email': 'testemail@gmail.com',
#         #     'username': 'username',
#         #     'password': 'tes',
#         #     'password2': 'tes',
#         #     'name': 'fullname'
#         # }
#         # self.user_unmatching_password = {
#         #     'email': 'testemail@gmail.com',
#         #     'username': 'username',
#         #     'password': 'teslatt',
#         #     'password2': 'teslatto',
#         #     'name': 'fullname'
#         # }

#         # self.user_invalid_email = {
#         #     'email': 'test.com',
#         #     'username': 'username',
#         #     'password': 'teslatt',
#         #     'password2': 'teslatto',
#         #     'name': 'fullname'
#         # }

#         self.user = User.objects.create(
#             first_name=self.correct_user_data['first_name'],
#             last_name=self.correct_user_data['last_name'],
#             email=self.correct_user_data['email'],
#             username=self.correct_user_data['email'],
#             password=self.correct_user_data['password']
#         )
#         return super().setUp()
class BaseTest(TestCase):

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Bienvenido',
            last_name='Sáez Muelas',
            email='bienvenidosaez@baetica.com',
            username='bienvenidosaez@baetica.com',
            password='admin123'
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
                'username': 'bienvenidosaez@baetica.com',
                'password': 'admin123',
            }
        )
        assert resp.status_code == 302
        self.assertRedirects(resp, '/dashboard/')

        # self.assertEqual(response.resolver_match.func.__name__,
        #  MyView.as_view().__name__)

        # assert resp.context['user'] == self.user
        # self.assertIn('SESSION_KEY', self.client.session)


class DashboardViewTest(BaseTest):

    def test_anonymous(self):
        resp = self.client.get(reverse('users:dashboard'))
        # self.assertTemplateUsed(resp, 'users/UserLogin.html')
        assert resp.status_code == 302
        self.assertRedirects(resp, '/login/?next=/dashboard/')

    def test_with_user_register(self):
        self.client.login(
            username='bienvenidosaez@baetica.com',
            password='admin123'
        )
        resp = self.client.get(reverse('users:dashboard'))
        assert resp.context['user'] == self.user
        self.assertTemplateUsed(resp, 'users/Dashboard.html')
        assert resp.status_code == 200

    # def logout(self):
    #     response = self.client.get('/admin/logout/')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertNotIn(SESSION_KEY, self.client.session)
    # def test_login_success(self):
    #     # self.client.post(self.register_url, self.user, format='text/html')
    #     # user = User.objects.filter(email=self.user['email']).first()
    #     # user.is_active = True
    #     # user.save()
    #     response = self.client.post(
    #         self.login_url, self.user, format='text/html')
    #     self.assertEqual(response.status_code, 302)

    # def test_cantlogin_with_unverified_email(self):
    #     self.client.post(self.register_url, self.user, format='text/html')
    #     response = self.client.post(
    #         self.login_url, self.user, format='text/html')
    #     self.assertEqual(response.status_code, 401)

    # def test_cantlogin_with_no_username(self):
    #     response = self.client.post(
    #         self.login_url, {'password': 'passwped', 'username': ''}, format='text/html')
    #     self.assertEqual(response.status_code, 401)

    # def test_cantlogin_with_no_password(self):
    #     response = self.client.post(
    #         self.login_url, {'username': 'passwped', 'password': ''}, format='text/html')
    #     self.assertEqual(response.status_code, 401)


# class TestDashboardView(UserTestModel):

#     def test_login_view_with_anonymous(self):
#         req = RequestFactory().get(reverse("users:dashboard"))
#         req.user = AnonymousUser()
#         resp = DashboardView.as_view()(req)
#         assert resp.status_code == 302, "Si está logueado, debe redireccionar"
#         assert "login" in resp.url

#     def test_login_view_with_user_register(self):
#         req = RequestFactory().get(reverse("users:dashboard"))
#         req.user = self.user
#         resp = DashboardView.as_view()(req)
#         assert resp.status_code == 200

    # def test_booking_detail_view(self):
    #     kwargs={'code': self.booking.code}
    #     self.booking.status='PA'
    #     self.booking.save()
    #     url = reverse_lazy('bookings:detail', kwargs=kwargs)
    #     request = self.rf.get(url)
    #     response = Detail.as_view()(request, **kwargs)
    #     self.assertEqual(response.status_code, 200)

    # def test_booking_payment_view_redirect(self):
    #     kwargs={'code': self.booking.code}
    #     self.booking.status='PA'
    #     self.booking.save()
    #     url = reverse_lazy('bookings:payment', kwargs=kwargs)
    #     request = self.rf.get(url)
    #     response = Payment.as_view()(request, **kwargs)
    #     self.assertEqual(response.status_code, 302)

    # def test_booking_payment_view(self):
    #     kwargs={'code': self.booking.code}
    #     self.booking.status='PE'
    #     self.booking.save()
    #     url = reverse_lazy('bookings:payment', kwargs=kwargs)
    #     request = self.rf.get(url)
    #     response = Payment.as_view()(request, **kwargs)
    #     self.assertEqual(response.status_code, 200)

    # def test_home(self):
    #     c = Client()
    #     response = c.get('/es/')
    #     self.assertEqual(response.status_code, 200)

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
