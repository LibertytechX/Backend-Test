from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from core.models import User

class CreateUsersTestCases(APITestCase):

    def setUp(self) -> None:
        self.url = reverse("create_user")
        self.good_data =  {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword'
        }

        self.invalid_data = {
            'username': 'testuser',
            'password': 'short'
        }

    def test_create_user_successful(self):

        response = self.client.post(self.url, self.good_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(User.objects.count(), 1)

        # Verify response data
        self.assertEqual(response.data['message'], 'Created user successfully')
        self.assertEqual(response.data['username'], self.good_data['username'])

    def test_create_user_invalid_payload(self):
        # Test creating a user with invalid payload

        response = self.client.post(self.url, self.invalid_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('email', response.data['message'])

    def test_create_user_exception_handling(self):
        
        # Test exception handling in create user view.

        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword'
        }

        # Create a user first to cause IntegrityError on duplicate creation
        User.objects.create_user(**user_data)

        response = self.client.post(self.url, user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Email Address or Username already exists.', response.data['message'])

    