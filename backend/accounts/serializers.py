from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import serializers

from .models import PasswordResetToken, User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    confirm_password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password", "confirm_password"]

    def validate_email(self, value):
        if User.objects.filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value

    def validate(self, attrs):
        if attrs["password"] != attrs["confirm_password"]:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        password_validation.validate_password(attrs["password"])
        return attrs

    def create(self, validated_data):
        validated_data.pop("confirm_password")
        return User.objects.create_user(**validated_data, role=User.Role.USER)


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(label="Username or Email")
    password = serializers.CharField(write_only=True)
    remember_me = serializers.BooleanField(default=False)


class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "full_name", "role", "is_active"]


class UpdateProfileSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=False, allow_blank=False, min_length=8)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def update(self, instance, validated_data):
        validated_data.pop("confirm_password", None)
        password = validated_data.pop("password", None)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        if password:
            password_validation.validate_password(password, instance)
            instance.password = make_password(password)
        instance.save()
        return instance


class ForgotPasswordRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ForgotPasswordConfirmSerializer(serializers.Serializer):
    token = serializers.UUIDField()
    new_password = serializers.CharField(min_length=8)

    def validate_token(self, value):
        try:
            token = PasswordResetToken.objects.select_related("user").get(token=value)
        except PasswordResetToken.DoesNotExist as exc:
            raise serializers.ValidationError("Invalid reset token.") from exc
        if not token.is_valid:
            raise serializers.ValidationError("Reset token has expired or already been used.")
        self.context["token_obj"] = token
        return value

    def validate_new_password(self, value):
        password_validation.validate_password(value)
        return value

    def save(self):
        token_obj = self.context["token_obj"]
        user = token_obj.user
        user.password = make_password(self.validated_data["new_password"])
        user.save(update_fields=["password"])
        token_obj.used_at = timezone.now()
        token_obj.save(update_fields=["used_at"])
        return user


class AdminUserSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "full_name",
            "first_name",
            "last_name",
            "email",
            "role",
            "is_active",
            "date_joined",
        ]


class AdminUpdateUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False, allow_blank=False, min_length=8)
    confirm_password = serializers.CharField(write_only=True, required=False, allow_blank=False, min_length=8)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "password", "confirm_password", "is_active", "role"]

    def validate(self, attrs):
        password = attrs.get("password")
        confirm_password = attrs.get("confirm_password")

        if password or confirm_password:
            if password != confirm_password:
                raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        return attrs

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email__iexact=value).exists():
            raise serializers.ValidationError("Email already in use.")
        return value

    def update(self, instance, validated_data):
        validated_data.pop("confirm_password", None)
        password = validated_data.pop("password", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            password_validation.validate_password(password, instance)
            instance.password = make_password(password)
        instance.save()
        return instance
