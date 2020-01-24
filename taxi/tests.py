# Create your tests here.
from unittest import TestCase

from django.contrib.auth.models import User


class AuthTestCase(TestCase):
    def setUp(self):
        self.u = User.objects.create_user('04', '01', 'test@dom.com', '01', 'pass')
        self.u.is_staff = True
        self.u.is_superuser = True
        self.u.is_active = True
        self.u.save()

    def testLogin(self):
        self.client.login(username='test@dom.com', password='pass')
