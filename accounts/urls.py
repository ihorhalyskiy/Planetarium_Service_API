from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.views import CreateUserView

app_name = "accounts"

urlpatterns = [
    path(
        "register/",
        CreateUserView.as_view(),
        name="create"
    ),
    path(
        "token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair"
    ),
    path(
        "token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh"
    ),
    path(
        "token/verify/",
        TokenVerifyView.as_view(),
        name="token_verify"
    ),
]
