
from rest_framework.test import APITestCase

from core.utils import get_serializer_key_error, response_data


class TestGetSerializerKeyError(APITestCase):

    def test_valid_errors_dict(self):
        # Test when a valid errors dictionary is provided.

        errors_dict = {
            'username': ['This field is required.'],
            'email': ['Enter a valid email address.']
        }
        result = get_serializer_key_error(errors_dict)
        self.assertEqual(result, '`username` -> This field is required.')

    def test_empty_errors_dict(self):
        # Test when an empty errors dictionary is provided.

        errors_dict = {}
        result = get_serializer_key_error(errors_dict)
        self.assertEqual(result, '')
    
    def test_empty_error_message(self):
        # Test when an errors dictionary has an empty error message list.
        
        errors_dict = {
            'username': []
        }
        result = get_serializer_key_error(errors_dict)
        self.assertEqual(result, '')

    def test_missing_key(self):
        # Test when errors dictionary has no keys.
        
        errors_dict = {}
        result = get_serializer_key_error(errors_dict)
        self.assertEqual(result, '')

    def test_invalid_errors_dict(self):
        # Test when errors dictionary is not in expected format.
        
        errors_dict = None
        result = get_serializer_key_error(errors_dict)
        self.assertEqual(result, '')


class TestResponseDataFunction(APITestCase):

    def test_response_data_structure(self):
        # Test the structure of the response data.
        
        message = "Test message"
        status_code = 200

        data = response_data(message, status_code)

        self.assertIn('message', data)
        self.assertIn('status-code', data)
        self.assertEqual(data['message'], message)
        self.assertEqual(data['status-code'], status_code)

    def test_response_data_message_type(self):
        # Test the type of the message in the response data.
        
        message = "Test message"
        status_code = 200

        data = response_data(message, status_code)

        self.assertIsInstance(data['message'], str)

    def test_response_data_status_code(self):
        # Test the type and range of status code in the response data.
        
        message = "Test message"
        status_code = 200

        data = response_data(message, status_code)

        self.assertIsInstance(data['status-code'], int)
        self.assertGreaterEqual(data['status-code'], 100)
        self.assertLessEqual(data['status-code'], 599)
