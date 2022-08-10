from django.test import TestCase
from django.test import Client

# Model
from krm.users.models import User


class UserTestModel(TestCase):

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Bienvenido',
            last_name='Sáez Muelas',
            email='bienvenidosaez@baetica.com',
            username='bienvenidosaez@baetica.com',
            password='admin123'
        )
