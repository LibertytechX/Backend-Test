from .serializers import UserSerializer

from django.db import IntegrityError
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny

from .utils import get_serializer_key_error, response_data


class CreateUser(generics.GenericAPIView):

    permission_classes = (AllowAny,)
    # serializer_class = UserSerializer

    def post(self, request):

        try:
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data.get("username")
            serializer.save()
            data = {
                "message": "Created user successfully",
                "username": username,
                "status-code": 200
            }
            return Response(data, status=status.HTTP_200_OK)
            
        except ValidationError:
            data = response_data(
                message=f"Invalid Request Payload: {get_serializer_key_error(serializer.errors)}",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except IntegrityError as err:
            data = response_data(
                message="Email Address or Username already exists.",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        except Exception as err:
            data = response_data(
                message=f"Failed to create User: {str(err)}",
                status_code=400
            )
            return Response(data, status=status.HTTP_400_BAD_REQUEST)
        


