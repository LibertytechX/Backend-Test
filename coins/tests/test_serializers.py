from rest_framework.test import APITestCase
from coins.serializers import FavouriteCoinSerializer


class FavouriteCoinsSerializerTests(APITestCase):

    def test_serializer_create_valid(self):
        data = {
            'username': 'testuser',
            'favourite': 'Bitcoin'
        }
        serializer = FavouriteCoinSerializer(data=data)

        self.assertTrue(serializer.is_valid())

    def test_serializer_create_invalid(self):
        data = {
            'user': "testuser"
        }
        serializer = FavouriteCoinSerializer(data=data)

        self.assertFalse(serializer.is_valid())
        self.assertIn('favourite', serializer.errors)