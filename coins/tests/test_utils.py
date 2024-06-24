from rest_framework.test import APITestCase

from unittest.mock import patch, MagicMock
from coins.utils import CoinAPI, env



class TestCoinAPI(APITestCase):

    def setUp(self):
        self.mock_base_url = "https://api.coinapi.io"
        self.mock_api_key = env("COIN_API_KEY")
        self.expected_headers = {
            "Accept": "text/plain",
            "X-CoinAPI-Key": self.mock_api_key
        }

    @patch('requests.get')
    def test_fetch_coin_by_id_success(self, mock_get):
        coin_id = "bitcoin"
        expected_url = f"{self.mock_base_url}/v1/assets/{coin_id}"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response
        
        result = CoinAPI.fetch_coin_by_id(coin_id)

        mock_get.assert_called_once_with(expected_url, headers=self.expected_headers)
        self.assertEqual(result, [])

    @patch('requests.get')
    def test_fetch_coin_by_id_invalid_response(self, mock_get):
        coin_id = 12
        expected_url = f"{self.mock_base_url}/v1/assets/{coin_id}"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = None
        mock_get.return_value = mock_response

        result = CoinAPI.fetch_coin_by_id(coin_id)

        mock_get.assert_called_once_with(expected_url, headers=self.expected_headers)
        self.assertEqual(result, None)

    @patch('requests.get')
    def test_fetch_all_coins_success(self, mock_get):
        expected_url = f"{self.mock_base_url}/v1/assets"
        mock_response_data = [] 

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = []
        mock_get.return_value = mock_response

        # mock_get.return_value = self.mock_response(200, mock_response_data)
        result = CoinAPI.fetch_all_coins()

        mock_get.assert_called_once_with(expected_url, headers=self.expected_headers)
        self.assertEqual(result, mock_response_data)