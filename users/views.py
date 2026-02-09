from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from .serializers import *
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

# Create your views here.


class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "registered"
            },
            status=status.HTTP_201_CREATED
        )

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        access = serializer.validated_data['access_token']
        refresh = serializer.validated_data['refresh_token']

        response = Response(
            {
                'username': serializer.validated_data['user'].username,
                'access_token': access
            },
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key='refresh_token',
            value=refresh,
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=7*24*60*60
        )
        return response

class TokenRefreshView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response(
                {'detail': 'refresh token not found'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        serializer = RefreshSerializer(data={'token': refresh_token})
        serializer.is_valid(raise_exception=True)
        response = Response(
            {"access": serializer.validated_data['new_access']},
            status=status.HTTP_200_OK
        )

        response.set_cookie(
            key="refresh_token",
            value=serializer.validated_data['new_refresh'],
            httponly=True,
            secure=True,
            samesite="Lax"
        )

        return response

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")

        response = Response(
            {"detail": "Successfully logged out"},
            status=status.HTTP_200_OK
        )

        if not refresh_token:
            response.delete_cookie("refresh_token")
            return response

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()

        except TokenError:
            pass

        response.delete_cookie("refresh_token")

        return response