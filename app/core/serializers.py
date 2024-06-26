# api/serializers.py
from rest_framework import serializers

from .models import Coin, Favourite, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        return user


class CoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = Coin
        exclude = ("id",)


class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourite
        exclude = ("id",)
