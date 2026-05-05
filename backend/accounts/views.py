from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.utils.decorators import method_decorator
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import PasswordResetToken, User, generate_secure_password
from .permissions import IsAdminUserRole
from .serializers import (
    AdminUpdateUserSerializer,
    AdminUserSerializer,
    ForgotPasswordConfirmSerializer,
    ForgotPasswordRequestSerializer,
    LoginSerializer,
    RegisterSerializer,
    UpdateProfileSerializer,
    UserProfileSerializer,
)


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {"message": "Registration successful.", "user": UserProfileSerializer(user).data},
            status=status.HTTP_201_CREATED,
        )


@method_decorator(ensure_csrf_cookie, name="dispatch")
class CsrfTokenView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        from django.middleware.csrf import get_token
        return Response({"csrfToken": get_token(request)})


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        identifier = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        remember_me = serializer.validated_data["remember_me"]

        # Try to find user by username or email
        user_obj = User.objects.filter(Q(username__iexact=identifier) | Q(email__iexact=identifier)).first()

        if user_obj and not user_obj.is_active:
            return Response({"message": "This account was disabled by admin."}, status=status.HTTP_403_FORBIDDEN)

        # Use the actual username for authentication
        username = user_obj.username if user_obj else identifier
        user = authenticate(request, username=username, password=password)
        if not user:
            return Response({"message": "Invalid username or password."}, status=status.HTTP_400_BAD_REQUEST)

        login(request, user)
        request.session.set_expiry(31536000 if remember_me else 0)
        return Response({"message": "Login successful.", "user": UserProfileSerializer(user).data})


class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful."})


class CurrentUserView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer

    def get_object(self):
        return self.request.user


class UpdateCurrentUserView(generics.UpdateAPIView):
    serializer_class = UpdateProfileSerializer

    def get_object(self):
        return self.request.user

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {"message": "Profile updated.", "user": UserProfileSerializer(self.get_object()).data}
        return response


class ForgotPasswordRequestView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            return Response({"message": "No account found with this email."}, status=status.HTTP_404_NOT_FOUND)

        new_password = f"{user.username}@123456789"
        user.password = make_password(new_password)
        user.save(update_fields=["password"])

        return Response(
            {
                "message": "Password reset successful.",
                "username": user.username,
                "generated_password": new_password,
            }
        )


class ForgotPasswordConfirmView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = ForgotPasswordConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password reset successful."})


class AdminUserListView(generics.ListAPIView):
    serializer_class = AdminUserSerializer
    permission_classes = [IsAdminUserRole]

    def get_queryset(self):
        from django.db.models.functions import Replace
        from django.db.models import Value

        query = self.request.query_params.get("search", "").strip()
        clean_query = query.replace(" ", "")
        queryset = User.objects.all().order_by("id")

        if query:
            queryset = queryset.annotate(
                c_first=Replace("first_name", Value(" "), Value("")),
                c_last=Replace("last_name", Value(" "), Value("")),
                c_email=Replace("email", Value(" "), Value("")),
                c_username=Replace("username", Value(" "), Value("")),
            ).filter(
                Q(c_first__icontains=clean_query)
                | Q(c_last__icontains=clean_query)
                | Q(c_email__icontains=clean_query)
                | Q(c_username__icontains=clean_query)
            )
        return queryset


class AdminUserDetailUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminUpdateUserSerializer
    permission_classes = [IsAdminUserRole]
    queryset = User.objects.all()

    def retrieve(self, request, *args, **kwargs):
        user = self.get_object()
        return Response(AdminUserSerializer(user).data)

    def update(self, request, *args, **kwargs):
        response = super().update(request, *args, **kwargs)
        response.data = {"message": "User updated successfully.", "user": AdminUserSerializer(self.get_object()).data}
        return response


class AdminToggleUserActiveView(APIView):
    permission_classes = [IsAdminUserRole]

    def patch(self, request, user_id):
        user = get_object_or_404(User, id=user_id)
        user.is_active = not user.is_active
        user.save(update_fields=["is_active"])
        return Response(
            {
                "message": f"User {'activated' if user.is_active else 'inactivated'} successfully.",
                "user": AdminUserSerializer(user).data,
            }
        )
