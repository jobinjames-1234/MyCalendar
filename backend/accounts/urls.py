from django.urls import path

from .views import (
    AdminToggleUserActiveView,
    AdminUserDetailUpdateView,
    AdminUserListView,
    CsrfTokenView,
    CurrentUserView,
    ForgotPasswordConfirmView,
    ForgotPasswordRequestView,
    LoginView,
    LogoutView,
    RegisterView,
    UpdateCurrentUserView,
)

urlpatterns = [
    path("csrf/", CsrfTokenView.as_view(), name="csrf"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("forgot-password/request/", ForgotPasswordRequestView.as_view(), name="forgot-password-request"),
    path("forgot-password/confirm/", ForgotPasswordConfirmView.as_view(), name="forgot-password-confirm"),
    path("me/", CurrentUserView.as_view(), name="current-user"),
    path("me/update/", UpdateCurrentUserView.as_view(), name="update-current-user"),
    path("admin/users/", AdminUserListView.as_view(), name="admin-users-list"),
    path("admin/users/<int:pk>/", AdminUserDetailUpdateView.as_view(), name="admin-user-detail-update"),
    path("admin/users/<int:user_id>/toggle-active/", AdminToggleUserActiveView.as_view(), name="admin-toggle-user-active"),
]
