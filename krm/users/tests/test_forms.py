from django.test import TestCase
from django.test import Client

from krm.users.forms import LoginForm


class LoginFormTest(TestCase):
    def test_UserForm_valid(self):
        form = LoginForm(
            data={
                'username': "user@mp.com",
                'password': "user",
            }
        )
        self.assertTrue(form.is_valid())

    def test_UserForm_invalid(self):
        form = LoginForm(
            data={
                'username': "",
                'password': "user",
            }
        )
        self.assertFalse(form.is_valid())
