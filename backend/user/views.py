from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
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

            # Set tokens in HTTP-only cookies
            response = Response(
                {"message": "Signup successful", "user": UserSerializer(user).data},
                status=status.HTTP_201_CREATED,
            )

            response.set_cookie(
                "access_token",
                str(access_token),
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
                httponly=True,
                secure=True,
                samesite="Strict",
            )

            response.set_cookie(
                "refresh_token",
                str(refresh),
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                httponly=True,
                secure=True,
                samesite="Strict",
            )

            return response

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

            # Set tokens in HTTP-only cookies
            response = Response(
                {"message": "Login successful", "user": UserSerializer(user).data},
                status=status.HTTP_200_OK,
            )

            response.set_cookie(
                "access_token",
                str(access_token),
                max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
                httponly=True,
                secure=True,
                samesite="Strict",
            )

            response.set_cookie(
                "refresh_token",
                str(refresh),
                max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
                httponly=True,
                secure=True,
                samesite="Strict",
            )

            return response

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
    response = Response(
        {"message": "Logged out successfully"}, status=status.HTTP_200_OK
    )
    response.delete_cookie("access_token")
    response.delete_cookie("refresh_token")
    return response


@api_view(["POST"])
@permission_classes([AllowAny])
def request_password_reset(request):
    serializer = PasswordResetRequestSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.validated_data["email"]
        try:
            user = User.objects.get(email=email)

            # Generate password reset token
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))

            # Create reset link
            reset_url = request.build_absolute_uri(
                reverse(
                    "password_reset_confirm", kwargs={"uidb64": uid, "token": token}
                )
            )

            # Send email
            send_mail(
                "Password Reset Request",
                f"""
                Hi {user.first_name},

                You requested to reset your password. Click the link below to reset it:

                {reset_url}

                If you did not request this, please ignore this email.

                Regards,
                Your App Team
                """,
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
        except User.DoesNotExist:
            pass  # Don't reveal if email exists

        return Response(
            {
                "message": "If an account with this email exists, a reset link has been sent."
            },
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response(
            {"error": "Invalid reset link"}, status=status.HTTP_400_BAD_REQUEST
        )

    if not default_token_generator.check_token(user, token):
        return Response(
            {"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST
        )

    serializer = PasswordResetSerializer(data=request.data)
    if serializer.is_valid():
        new_password = serializer.validated_data["new_password"]
        user.set_password(new_password)
        user.save()

        return Response(
            {"message": "Password has been reset successfully"},
            status=status.HTTP_200_OK,
        )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
    users = User.objects.all()
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
def promote_user(request, user_id):
    """Admin can promote a user to admin role"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.role = "admin"
    user.save()

    return Response(
        {
            "message": f"User {user.username} promoted to admin",
            "user": UserSerializer(user).data,
        }
    )


@api_view(["POST"])
@permission_classes([IsAdmin])
def demote_user(request, user_id):
    """Admin can demote an admin to regular user"""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

    user.role = "user"
    user.save()

    return Response(
        {
            "message": f"User {user.username} demoted to regular user",
            "user": UserSerializer(user).data,
        }
    )


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
