from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
import jwt
from datetime import datetime, timedelta
from .serializers import (
    UserSignupSerializer,
    UserLoginSerializer,
    UserSerializer,
    PasswordResetRequestSerializer,
    PasswordResetSerializer,
)
from .permissions import IsAdmin, IsAdminOrReadOnly, IsOwnerOrAdmin

User = get_user_model()


class SignupView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()

            # Create JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Return tokens in response body instead of cookies
            return Response(
                {
                    "message": "Signup successful",
                    "user": UserSerializer(user).data,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
                    "token_type": "Bearer",
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.GenericAPIView):
    serializer_class = UserLoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]

            # Create JWT tokens
            refresh = RefreshToken.for_user(user)
            access_token = refresh.access_token

            # Return tokens in response body instead of cookies
            return Response(
                {
                    "message": "Login successful",
                    "user": UserSerializer(user).data,
                    "access_token": str(access_token),
                    "refresh_token": str(refresh),
                    "token_type": "Bearer",
                },
                status=status.HTTP_200_OK,
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserMeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response({"user": serializer.data}, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Logout view - since tokens are stored in localStorage,
    the frontend will handle removing them.
    Optionally, you can blacklist the refresh token here.
    """
    try:
        # Get refresh token from request body
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            # Blacklist the refresh token
            token = RefreshToken(refresh_token)
            token.blacklist()

        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )
    except TokenError:
        return Response(
            {"message": "Logged out successfully"}, status=status.HTTP_200_OK
        )


class TokenRefreshView(APIView):
    """
    Refresh access token using refresh token from request body
    """

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return Response(
                {"detail": "Refresh token is required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            refresh = RefreshToken(refresh_token)
            new_access = refresh.access_token

            response_data = {"access_token": str(new_access), "token_type": "Bearer"}

            # Optional: Rotate refresh token for better security
            # Uncomment the following lines if you want to rotate refresh tokens
            # new_refresh = RefreshToken.for_user(User.objects.get(id=refresh['user_id']))
            # response_data["refresh_token"] = str(new_refresh)

            return Response(response_data, status=status.HTTP_200_OK)

        except TokenError:
            return Response(
                {"detail": "Refresh token expired or invalid."},
                status=status.HTTP_401_UNAUTHORIZED,
            )


# Optional: Blacklist token view for better logout security
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def blacklist_token_view(request):
    """
    Blacklist a refresh token to prevent its future use
    """
    try:
        refresh_token = request.data.get("refresh_token")
        if refresh_token:
            token = RefreshToken(refresh_token)
            token.blacklist()

        return Response(
            {"message": "Token blacklisted successfully"}, status=status.HTTP_200_OK
        )
    except TokenError:
        return Response({"detail": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def user_profile(request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)


# Admin-only views
@api_view(["GET"])
@permission_classes([IsAdmin])
def list_all_users(request):
    """Admin can view all users"""
    users = User.objects.filter(role="user")
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAdmin])
def manage_user(request, user_id):
    """Admin can view, update, or delete any user"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = UserSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(
            {"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT
        )


@api_view(["POST"])
@permission_classes([IsAdmin])
def create_user(request):
    """Admin can create new users"""
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        # Set default role to 'user' if not provided
        user = serializer.save(role="user")
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User can update their own profile
@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """User can update their own profile"""
    serializer = UserSerializer(request.user, data=request.data, partial=True)
    if serializer.is_valid():
        # Prevent users from changing their own role
        if "role" in serializer.validated_data and not request.user.is_admin:
            return Response(
                {"error": "You cannot change your own role"},
                status=status.HTTP_403_FORBIDDEN,
            )
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
