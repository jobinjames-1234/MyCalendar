from django.contrib import admin

from .models import PasswordResetToken, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_active", "is_staff")
    list_filter = ("role", "is_active")
    search_fields = ("username", "email", "first_name", "last_name")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "token", "expires_at", "used_at", "created_at")
    search_fields = ("user__username", "user__email")
    list_filter = ("used_at",)
