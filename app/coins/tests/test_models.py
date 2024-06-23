# from django.contrib.auth.models import User
from core.models import User
from rest_framework.test import APITestCase
from rest_framework import status
from coins.models import FavouriteCoins  

from django.db import IntegrityError


class FavouriteCoinsTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(email='testuser@gmail.com', username='testuser', password='password123')
        self.favourite = FavouriteCoins.objects.create(user=self.user, coin_name="Bitcoin")

    def test_create_favourite_coin(self):
        coin_name = "Bitcoin"
        
        self.assertEqual(self.favourite.coin_name, coin_name)
        self.assertEqual(FavouriteCoins.objects.filter(user=self.user, coin_name=coin_name).count(), 1)

    def test_unique_constraint(self):
        coin_name = "Bitcoin"

        with self.assertRaises(IntegrityError):
            FavouriteCoins.objects.create(user=self.user, coin_name=coin_name)

    def test_get_favourite_coins(self):
        coin_name = "Bitcoin"
        coin = FavouriteCoins.objects.get(coin_name=coin_name)

        self.assertEqual(coin.coin_name, coin_name)