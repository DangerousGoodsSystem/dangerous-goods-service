from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import (
    LoginUserView,
    LogoutUserView,
    PasswordChangeView,
    PasswordResetRequestView,
    SetNewPasswordView,
)

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('logout/', LogoutUserView.as_view(), name='logout-user'),
    path('token-refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-change/', PasswordChangeView.as_view(), name='password-change'),
    path('password-reset-request/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset-complete/', SetNewPasswordView.as_view(), name='password-reset-complete'),
]
