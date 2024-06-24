from django.db import IntegrityError
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated

from core.models import User
from .models import FavouriteCoins
from .serializers import FavouriteCoinSerializer
from core.utils import get_serializer_key_error, response_data
from .utils import (
    currency_formatter,
    CoinAPI
)

# Create your views here.


class AddFavouriteCoin(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]
    serializer_class = FavouriteCoinSerializer

    def post(self, request):
        try:
            serializer = FavouriteCoinSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data.get("username")
            coin_name = serializer.validated_data.get("favourite").upper()
            user = User.objects.get(username=username)
            # coins = fetch_coin_by_id(coin_name)
            coins = CoinAPI.fetch_coin_by_id(coin_name)
            if (
                type(coins) is list
                and len(coins) > 0
                # Coin API returns an Array but just one item always.
            ):
                FavouriteCoins.objects.create(
                    user=user, coin_name=coin_name
                )
                data = {
                    "message": f"Added {coin_name} to Favourite successfully",
                    "username": username,
                    "coin-name": coin_name,
                    "status-code": 200
                }
                return Response(data, status=status.HTTP_200_OK)
            
            elif (
                type(coins) is list
                and len(coins) == 0
            ):
                data = response_data(
                    message=f"Coin name {coin_name} not found",
                    status_code=404
                )
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                data = response_data(
                    message="Something went wrong fetching the coin",
                    status_code=500
                )
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        except ValidationError:
            data = response_data(
                message=f"Invalid Request Payload: {get_serializer_key_error(serializer.errors)}",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            data = response_data(
                message="Username not found",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError:
            data = response_data(
                message=f"User already have {coin_name} saved to favourites",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            data = response_data(
                message=f"Failed add to favourites: {str(err)}",
                status_code=500
            )
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        


class ListFavouriteCoins(viewsets.GenericViewSet):

    permission_classes = [IsAuthenticated]

    def get_queryset(self, username):
        fav_coins = FavouriteCoins.objects.filter(user__username=username
            ).order_by('-date_created')
        
        return fav_coins
    
    def list(self, request):
        """
        An Async approach was intended here as defined in utils, but the Coin API has rate limiting 
        for a small amount of time and returns a 429.
        """
        try:
            username = request.data.get("username")
            User.objects.get(username=username)
            # Just to be able to return an appriopriate message if username not found

            coin_list = []
            query_set = self.get_queryset(username=username)
            if query_set:
                for q in query_set:
                    coin_name = q.coin_name
                    coins = CoinAPI.fetch_coin_by_id(coin_name)
                    coin = coins[0]
                    data = {
                        "name": coin["asset_id"],
                        "USD-PRICE": currency_formatter(coin.get("price_usd", "No price")), 
                        # USD Price not returned for all coins
                        "volume": currency_formatter(coin["volume_1mth_usd"])
                    }
                    coin_list.append(data)
                return Response(coin_list, status=status.HTTP_200_OK)
                    
            else:
                return Response(coin_list, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            data = response_data(
                message="User account not found.",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            data = response_data(
                message=f"Failed to return Favourites {err}",
                status_code=500
            )
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetAllCoins(generics.GenericAPIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            coin_list = []
            coins = CoinAPI.fetch_all_coins()
            for coin in coins:
                data = {
                    "name": coin["asset_id"],
                    "USD-PRICE": currency_formatter(coin.get("price_usd", "No price")), 
                    "volume": currency_formatter(coin["volume_1mth_usd"])
                }
                coin_list.append(data)
            return Response(coin_list, status=status.HTTP_200_OK)

        except Exception as err:
            data = response_data(
                message=f"Failed to fetch all coins {err}",
                status_code=500
            )
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#-----------------V2-----------------#        

class AddFavouriteCoinV2(generics.GenericAPIView):
    """
    This version is just how my approach to this API would look like; no JSON request body, 
    username is retrieved correctly and internally and coin is passed as path parameter.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request, coin: str):
        try:
            username = request.user.username
            coin_name = coin.upper()
            user = User.objects.get(username=username)
            coins = CoinAPI.fetch_coin_by_id(coin_name)
            if (
                type(coins) is list
                and len(coins) > 0
                # Coin API returns an Array but just one item always.
            ):
                FavouriteCoins.objects.create(
                    user=user, coin_name=coin_name
                )
                data = {
                    "message": f"Added {coin_name} to Favourite successfully",
                    "username": username,
                    "coin-name": coin_name,
                    "status-code": 200
                }
                return Response(data, status=status.HTTP_200_OK)
            
            elif (
                type(coins) is list
                and len(coins) == 0
            ):
                data = response_data(
                    message=f"Coin name {coin_name} not found",
                    status_code=404
                )
                return Response(data, status=status.HTTP_404_NOT_FOUND)
            else:
                data = response_data(
                    message="Something went wrong fetching the coin",
                    status_code=500
                )
                return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except IntegrityError:
            data = response_data(
                message=f"User already have {coin_name} saved to favourites",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            data = response_data(
                message=f"Failed add to favourites: {str(err)}",
                status_code=500
            )
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ListFavouriteCoinsV2(viewsets.GenericViewSet):
    """
    This version is just how my approach to this API would look like; JSON request body
    will not be used to retrieve user / username. It is retrieved internally
    """
    pagination_class = PageNumberPagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self, username):
        fav_coins = FavouriteCoins.objects.filter(user__username=username
            ).order_by('-date_created')
        
        return fav_coins
    
    def list(self, request):
        try:
            username = request.user.username
            coin_list = []
            query_set = self.get_queryset(username=username)
            if query_set:
                for q in query_set:
                    coin_name = q.coin_name
                    coins = CoinAPI.fetch_coin_by_id(coin_name)
                    coin = coins[0]
                    data = {
                        "name": coin["asset_id"],
                        "USD-PRICE": currency_formatter(coin.get("price_usd", "No price")), 
                        # USD Price not consistent for all coins
                        "volume": currency_formatter(coin["volume_1mth_usd"])
                    }
                    coin_list.append(data)
                return Response(coin_list, status=status.HTTP_200_OK)
                    
            else:
                return Response(coin_list, status=status.HTTP_200_OK)
        except Exception as err:
            data = response_data(
                message=f"Failed to return Favourites {err}",
                status_code=500
            )
            return Response(data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        

        
        

