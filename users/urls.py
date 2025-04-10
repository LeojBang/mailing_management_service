from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from users.apps import UsersConfig
from users.services import block_user, email_verification
from users.views import (CustomPasswordResetCompleteView,
                         CustomPasswordResetConfirmView,
                         CustomPasswordResetDoneView, CustomPasswordResetView,
                         EmailConfirmationView, ProfileView, RegisterView,
                         UsersListView)

app_name = UsersConfig.name

urlpatterns = [
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", RegisterView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email-confirm"),
    path(
        "email-confirmation/",
        EmailConfirmationView.as_view(),
        name="email_confirmation",
    ),
    path("list", (UsersListView.as_view()), name="users_list"),
    path("block_user/<int:pk>", block_user, name="block_user"),
    path("profile/", ProfileView.as_view(), name="profile"),
    path("password-reset/", CustomPasswordResetView.as_view(), name="password_reset"),
    path(
        "password-reset/done/",
        CustomPasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        CustomPasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
