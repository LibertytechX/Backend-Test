from rest_framework import serializers


class FavouriteCoinSerializer(serializers.Serializer):

    username = serializers.CharField(required=False)
    favourite = serializers.CharField(required=True)
    
    class Meta:
        fields = ['username', "favourite"]


