from django.core.exceptions import ObjectDoesNotExist
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.exceptions import ParseError, PermissionDenied, ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .models import Coin, Favourite, User
from .serializers import CoinSerializer, UserSerializer


@method_decorator(csrf_exempt, name="dispatch")
class RegisterView(generics.CreateAPIView):
    """Class to create new user"""

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs) -> Response:
        """Create new user"""
        try:
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    {
                        "message": "Created user successfully",
                        "username": serializer.data["username"],
                        "status-code": 200,
                    },
                    status=status.HTTP_201_CREATED,
                )
            return Response(
                {
                    "status": "error",
                    "response_code": "99",
                    "response": "User could not be created.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (ValidationError, KeyError, ParseError, PermissionDenied) as e:
            return Response(
                {"status": "error", "response_code": "99", "response": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class GetAllCoinsView(generics.ListAPIView):
    """Class to retrieve all the coins"""

    queryset = Coin.objects.all()
    serializer_class = CoinSerializer

    def get(self, request, *args, **kwargs):
        """Retrieve all coins form the db"""
        try:
            coins = self.get_queryset()
            serializer = self.get_serializer(coins, many=True)
            return Response(serializer.data)
        except (ParseError, PermissionDenied, ValidationError) as e:
            return Response(
                {"status": "error", "response_code": "99", "response": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class AddFavouriteView(generics.CreateAPIView):
    """Class to add a favourite coin to a user"""

    queryset = Favourite.objects.all()
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """Add a favourite coin to user account"""
        try:
            user = User.objects.get(username=request.data["username"])
            coin = Coin.objects.get(name=request.data["favourite"])
            favourite = Favourite(user=user, coin=coin)
            favourite.save()
            return Response(
                {
                    "message": f"Added {coin.name} to Favourite successfully",
                    "username": user.username,
                    "coin-name": coin.name,
                    "status-code": 200,
                },
                status=status.HTTP_200_OK,
            )
        except User.DoesNotExist:
            return Response(
                {"status": "error", "response_code": "99", "response": "User does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Coin.DoesNotExist:
            return Response(
                {"status": "error", "response_code": "99", "response": "Coin does not exist"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except (ValidationError, KeyError, ParseError, PermissionDenied) as e:
            return Response(
                {"status": "error", "response_code": "99", "response": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_exempt, name="dispatch")
class ViewFavouriteView(generics.ListAPIView):
    """Class to view a user's favourite coin/coins"""

    queryset = Favourite.objects.all()
    serializer_class = CoinSerializer

    def get(self, request, *args, **kwargs):
        """View user's favourite coins"""
        try:
            user = User.objects.get(username=request.data["username"])
            favourites = Favourite.objects.filter(user=user)
            subscribed_favourites = [f.coin for f in favourites]
            serializer = self.get_serializer(subscribed_favourites, many=True)
            return Response(
                {
                    "message": f"Welcome back {user.username} thanks for using our platform",
                    "subscribed_favourites": serializer.data,
                }
            )
        except (
            ObjectDoesNotExist,
            KeyError,
            ParseError,
            PermissionDenied,
            ValidationError,
        ) as e:
            return Response(
                {"status": "error", "response_code": "99", "response": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Favourite.DoesNotExist as e:
            return Response(
                {"status": "error", "response_code": "99", "response": str(e)},
                status=status.HTTP_400_BAD_REQUEST,
            )
