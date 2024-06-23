"""Tests for main app are found here."""

from django.test import TestCase
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from django.db.utils import IntegrityError
from core.models import User

class UserModelTestCase(APITestCase):

    def setUp(self):
        # Create a user for testing
        self.user = User.objects.create_user(email='test@example.com', username='testuser', password='password')
        self.superuser = User.objects.create_superuser(email='admin@example.com', username='admin', password='adminpassword')

    def test_create_user(self):
        # Test creating a user without specifying all fields
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.username, 'testuser')
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertTrue(self.user.is_active)

    def test_create_superuser(self):
        # Test creating a superuser
        self.assertEqual(self.superuser.email, 'admin@example.com')
        self.assertEqual(self.superuser.username, 'admin')
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_active)

    def test_create_superuser_missing_is_staff(self):
        # Test creating a superuser without is_staff=True
        with self.assertRaises(ValueError):
            User.objects.create_superuser(email='admin2@example.com', username='admin2', password='adminpassword', is_staff=False)

    def test_duplicate_email(self):
        # Test creating a user with a duplicate email should raise IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='test@example.com', username='anotheruser', password='password')

    def test_duplicate_username(self):
        # Test creating a user with a duplicate username should raise IntegrityError
        with self.assertRaises(IntegrityError):
            User.objects.create_user(email='another@example.com', username='testuser', password='password')

    def test_new_user_email_normalized(self):
        # Test the email for a new uer is normalized
        email = 'test@TEST.com'
        user = get_user_model().objects.create_user(email, 'test@test.com')

        self.assertEqual(user.email, email.lower())
