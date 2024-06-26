from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from core.models import Coin, Favourite, User
from core.serializers import CoinSerializer


class RegisterViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("register")

    def test_register_user_success(self):
        data = {
            "username": "testuser",
            "password": "password123",
            "email": "testuser@example.com",
        }
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["message"], "Created user successfully")
        self.assertEqual(response.data["username"], "testuser")
        self.assertEqual(response.data["status-code"], 200)
        self.assertTrue(User.objects.filter(username="testuser").exists())

    def test_register_user_missing_data(self):
        data = {"username": "testuser"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["response_code"], "99")
        self.assertIn("response", response.data)

    def test_register_user_invalid_data(self):
        data = {"username": "testuser", "password": "short", "email": "not-an-email"}
        response = self.client.post(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["status"], "error")
        self.assertEqual(response.data["response_code"], "99")
        self.assertIn("response", response.data)


class GetAllCoinsViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("get_all_coins")  # Use the appropriate URL name or path

        # Create sample coins
        Coin.objects.create(name="Bitcoin", usd_price="74847", volume="934579")
        Coin.objects.create(name="Ethereum", usd_price="3372", volume="73282362")

    def test_get_all_coins_success(self):
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        coins = Coin.objects.all()
        serializer = CoinSerializer(coins, many=True)
        self.assertEqual(response.data, serializer.data)

    def test_get_all_coins_no_content(self):
        Coin.objects.all().delete()  # Ensure no coins are present
        response = self.client.get(self.url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, [])


# class AddFavouriteViewTestCase(TestCase):
#     def setUp(self):
#         self.client = APIClient()
#         self.url = reverse("add_favourite")  # Use the appropriate URL name or path

#         # Create a sample user
#         self.user = User.objects.create_user(username="testuser", email='email@example.com', password="testpass")

#         # Create sample coins
#         self.coin1 = Coin.objects.create(name="Bitcoin", usd_price="74847", volume="934579")
#         self.coin2 = Coin.objects.create(name="Ethereum", usd_price="74856", volume="958583")

#     def test_add_favourite_success(self):
#         data = {"username": "testuser", "favourite": "Bitcoin"}
#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertTrue(
#             Favourite.objects.filter(user=self.user, coin=self.coin1).exists()
#         )
#         self.assertEqual(response.data["username"], "testuser")
#         self.assertEqual(response.data["coin-name"], "Bitcoin")

#     def test_add_favourite_invalid_user(self):
#         data = {"username": "invaliduser", "favourite": "Bitcoin"}
#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data["response_code"], "99")

#     def test_add_favourite_invalid_coin(self):
#         data = {"username": "testuser", "favourite": "InvalidCoin"}
#         response = self.client.post(self.url, data, format="json")

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
#         self.assertEqual(response.data["response_code"], "99")

class AddFavouriteViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse('add_favourite') 
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.coin = Coin.objects.create(name='Bitcoin', usd_price=30000, volume=700000)

    def test_add_favourite_success(self):
        data = {
            "username": self.user.username,
            "favourite": self.coin.name
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], f'Added {self.coin.name} to Favourite successfully')
        self.assertEqual(response.data['username'], self.user.username)
        self.assertEqual(response.data['coin-name'], self.coin.name)

    def test_add_favourite_invalid_user(self):
        data = {
            "username": "nonexistentuser",
            "favourite": self.coin.name
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')

    def test_add_favourite_invalid_coin(self):
        data = {
            "username": self.user.username,
            "favourite": "nonexistentcoin"
        }
        response = self.client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['status'], 'error')


class ViewFavouriteViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("view_favourites")  # Use the appropriate URL name or path

        # Create a sample user
        self.user = User.objects.create_user(username="testuser", email='email@exampl.com', password="testpass")

        # Create sample coins
        self.coin1 = Coin.objects.create(name="Bitcoin", usd_price="74847", volume="934579")
        self.coin2 = Coin.objects.create(name="Ethereum", usd_price="758", volume="54905")

        # Add favourites for the user
        Favourite.objects.create(user=self.user, coin=self.coin1)
        Favourite.objects.create(user=self.user, coin=self.coin2)


    def test_view_favourite_invalid_user(self):
        data = {"username": "invaliduser"}
        response = self.client.get(self.url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["response_code"], "99")

