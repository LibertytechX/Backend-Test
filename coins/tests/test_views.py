from core.models import User

from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from unittest.mock import patch
from coins.models import FavouriteCoins

from rest_framework_simplejwt.tokens import AccessToken


class AddFavouriteCoinTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email="testuser@gmail.com", password='password123')
        self.url = reverse("add_coin")

    def _get_jwt_token(self, user):
        token = AccessToken.for_user(user)
        return f'Bearer {token}'

    @patch("coins.views.CoinAPI.fetch_coin_by_id")
    def test_add_favourite_coin_success(self, mock_fetch_coin_by_id):
        coin_name = "Bitcoin"
        serializer_data = {
            'username': self.user.username,
            'favourite': coin_name
        }
        auth_token = self._get_jwt_token(self.user)
        mock_fetch_coin_by_id.return_value = [{'name': coin_name}]  

        response = self.client.post(self.url, serializer_data, format='json', HTTP_AUTHORIZATION=auth_token)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(f'Added {coin_name.upper()} to Favourite successfully', response.data['message'])
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['coin-name'], coin_name.upper())

    @patch("coins.views.CoinAPI.fetch_coin_by_id")
    def test_add_favourite_coin_coin_not_found(self, mock_fetch_coin_by_id):
        coin_name = "NonExistingCoin"
        serializer_data = {
            'username': self.user.username,
            'favourite': coin_name
        }

        mock_fetch_coin_by_id.return_value = [] 

        auth_token = self._get_jwt_token(self.user)
        response = self.client.post(self.url, serializer_data, format='json', HTTP_AUTHORIZATION=auth_token)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn(f'Coin name {coin_name.upper()} not found', response.data['message'])

    def test_add_favourite_coin_invalid_request_payload(self):
        serializer_data = {} 

        auth_token = self._get_jwt_token(self.user)
        response = self.client.post(self.url, serializer_data, format='json', HTTP_AUTHORIZATION=auth_token)
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Invalid Request Payload', response.data['message'])

    def test_add_favourite_coin_user_not_found(self):
        serializer_data = {
            'username': 'nonexistentuser',
            'favourite': 'Bitcoin'
        }

        auth_token = self._get_jwt_token(self.user)
        response = self.client.post(self.url, serializer_data, format='json', HTTP_AUTHORIZATION=auth_token)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Username not found', response.data['message'])


    @patch("coins.views.CoinAPI.fetch_coin_by_id")
    def test_add_favourite_coin_coin_api_failure(self, mock_fetch_coin_by_id):
        coin_name = "Bitcoin"
        serializer_data = {
            'username': self.user.username,
            'favourite': coin_name
        }

        mock_fetch_coin_by_id.side_effect = Exception("API failure")

        auth_token = self._get_jwt_token(self.user)
        response = self.client.post(self.url, serializer_data, format='json', HTTP_AUTHORIZATION=auth_token)

        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Failed add to favourites', response.data['message'])


class ListFavouriteCoinsTestCase(APITestCase):

    def setUp(self):
        # Create a user and some favourite coins for testing
        self.user = User.objects.create(username='testuser', password='testpassword', email='testuser@gmail.com')
        self.coin = FavouriteCoins.objects.create(user=self.user, coin_name='bitcoin')
        self.url = reverse('favourites_v2') 

    def _get_jwt_token(self, user):
        token = AccessToken.for_user(user)
        return f'Bearer {token}'
    
    @patch("coins.views.CoinAPI.fetch_coin_by_id")
    def test_list_favourite_coins_success(self, mock_fetch_coin_by_id):
        mock_fetch_coin_by_id.return_value = [
            {'asset_id': "bitcoin", "price_usd": 200000, "volume_1mth_usd": 34506777},
            {'asset_id': "SBC", "price_usd": 245000, "volume_1mth_usd": 345060007}
        ]
        auth_token = self._get_jwt_token(self.user)
        
        response = self.client.get(self.url, HTTP_AUTHORIZATION=auth_token)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['name'], 'bitcoin')
        self.assertIn('USD-PRICE', response.data[0])

    @patch("coins.views.CoinAPI.fetch_coin_by_id")
    def test_list_favourite_coins_internal_server_error(self, mock_fetch_coin_by_id):
        mock_fetch_coin_by_id.side_effect = Exception("Simulated internal server error")
        
        auth_token = self._get_jwt_token(self.user)
        response = self.client.get(self.url, HTTP_AUTHORIZATION=auth_token)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Failed to return Favourites', response.data['message'])


class GetAllCoinsTestCase(APITestCase):

    def setUp(self):
        self.url = reverse('all_coins') 
        self.user = User.objects.create(username='testuser', password='testpassword', email='testuser@gmail.com')

    def _get_jwt_token(self, user):
        token = AccessToken.for_user(user)
        return f'Bearer {token}'

    @patch("coins.views.CoinAPI.fetch_all_coins")
    def test_get_all_coins_success(self, mock_fetch_all_coins):
        mock_fetch_all_coins.return_value = [
            {"asset_id": "bitcoin", "price_usd": 50000, "volume_1mth_usd": 1000000},
            {"asset_id": "ethereum", "price_usd": 3000, "volume_1mth_usd": 500000}
        ]

        auth_token = self._get_jwt_token(self.user)
        response = self.client.get(self.url, HTTP_AUTHORIZATION=auth_token)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        self.assertEqual(response.data[0]['name'], 'bitcoin')
        self.assertIn('USD-PRICE', response.data[0])

    @patch("coins.views.CoinAPI.fetch_all_coins")
    def test_get_all_coins_internal_server_error(self, mock_fetch_all_coins):
        mock_fetch_all_coins.side_effect = Exception("Simulated internal server error")
        
        auth_token = self._get_jwt_token(self.user)
        response = self.client.get(self.url, HTTP_AUTHORIZATION=auth_token)
        
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('Failed to fetch all coins', response.data['message'])
