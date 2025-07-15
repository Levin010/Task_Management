from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt


urlpatterns = [
    path("signup/", views.SignupView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("profile/", views.user_profile, name="user_profile"),
    path("profile/update/", views.update_profile, name="update_profile"),
    path("me/", views.UserMeView.as_view(), name="user-me"),
    path(
        "token/refresh/",
        views.TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path("admin/users/", views.list_all_users, name="list_all_users"),
    path("admin/users/<int:user_id>/", views.manage_user, name="manage_user"),
    path("admin/users/create/", views.create_user, name="create_user"),
]
