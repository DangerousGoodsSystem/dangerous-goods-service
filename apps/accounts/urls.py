from django.urls import path
from .views import (
    LoginUserView,
    LogoutUserView,
)

urlpatterns = [
    path('login/', LoginUserView.as_view(), name='login-user'),
    path('logout/', LogoutUserView.as_view(), name='logout-user'),
]
