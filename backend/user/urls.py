from django.urls import path
from . import views

urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("me/", views.UserMeView.as_view(), name="user-me"),
    path(
        "request-password-reset/",
        views.request_password_reset,
        name="request_password_reset",
    ),
    path(
        "reset-password/<str:uidb64>/<str:token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),
    path("admin/users/", views.list_all_users, name="list_all_users"),
    path("admin/users/<int:user_id>/", views.manage_user, name="manage_user"),
    path("admin/users/<int:user_id>/promote/", views.promote_user, name="promote_user"),
    path("admin/users/<int:user_id>/demote/", views.demote_user, name="demote_user"),
]
