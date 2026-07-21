from django.test import TestCase
from django.test import Client

# Model
from krm.users.models import User


class UserTestModel(TestCase):

    def setUp(self):
        """Test case setup."""
        self.user = User.objects.create(
            first_name='Test',
            last_name='Test',
            email='no-replay-krctool@gcpv.com',
            username='no-replay-krctool@gcpv.com',
            password='test'
        )
