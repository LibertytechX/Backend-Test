from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import User


class UserSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(required=True)
    username = serializers.CharField(required=True)
    password = serializers.CharField(min_length=5, write_only=True, required=True)
    

    class Meta:
        model = User
        fields = ['username', 'password', 'email']

    
    def create(self, validated_data):
        _validated_data = validated_data
        password =_validated_data.pop('password')
        # Exclude password from model's object creation
        user = super().create(_validated_data)
        user.set_password(password)
        user.save()
        return user