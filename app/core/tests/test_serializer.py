from rest_framework.test import APITestCase

from core.serializers import UserSerializer

from core.models import User


class UserSerializerTestCase(APITestCase):


    def test_valid_user_serializer(self):
        # Test creating a user with valid serializer data.
        
        user_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'securepassword'
        }
        serializer = UserSerializer(data=user_data)
        self.assertTrue(serializer.is_valid())

        # Ensure user is created correctly
        created_user = serializer.save()

        # Check if the user exists in the database
        self.assertIsNotNone(created_user.id)
        self.assertEqual(created_user.username, user_data['username'])
        self.assertEqual(created_user.email, user_data['email'])

        # Check password hash
        self.assertTrue(created_user.check_password(user_data['password']))


    def test_missing_required_fields(self):
        # Test serializer validation when required fields are missing.

        user_data = {
            'username': 'testuser',
            'password': 'securepassword'
        }
        serializer = UserSerializer(data=user_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)