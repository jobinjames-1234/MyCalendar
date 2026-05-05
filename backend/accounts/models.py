import secrets
import string
import uuid
from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = "admin", "Admin"
        USER = "user", "User"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.USER)

    def save(self, *args, **kwargs):
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    expires_at = models.DateTimeField()
    used_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def mark_used(self):
        self.used_at = timezone.now()
        self.save(update_fields=["used_at"])

    @property
    def is_valid(self):
        return self.used_at is None and timezone.now() <= self.expires_at

    @classmethod
    def create_for_user(cls, user, expiry_minutes=30):
        return cls.objects.create(user=user, expires_at=timezone.now() + timedelta(minutes=expiry_minutes))


def generate_secure_password(length=14):
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(secrets.choice(alphabet) for _ in range(length))
