from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from .ratelimit import rate_limit_decorator
from .serializers import LoginSerializer, LogoutUserSerializer, PasswordChangeSerializer, PasswordResetRequestSerializer, SetNewPasswordSerializer

class LoginUserView(APIView):
    """
    View to handle user login and return JWT tokens.
    """
    serializer_class = LoginSerializer

    @rate_limit_decorator(rate='5/m')
    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LogoutUserView(APIView):
    """
    View to handle user logout and blacklist the refresh token.
    """
    serializer_class = LogoutUserSerializer

    @rate_limit_decorator(rate='5/m')
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Logout successful"}, status=status.HTTP_204_NO_CONTENT)

class PasswordChangeView(APIView):
    """
    API view allows logged in users to change their password.
    """
    permission_classes = [IsAuthenticated]
    serializer_class = PasswordChangeSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password changed successfully."}, status=status.HTTP_200_OK)


class PasswordResetRequestView(APIView):
    """
    API view for users to send password reset requests via email.
    """
    permission_classes = [AllowAny]
    serializer_class = PasswordResetRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {"message": "If your email exists in the system, you will receive a link to reset your password."},
            status=status.HTTP_200_OK
        )

class SetNewPasswordView(APIView):
    """
    API view to validate reset link and set new password.
    """
    permission_classes = [AllowAny]
    serializer_class = SetNewPasswordSerializer

    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Password was reset successfully."}, status=status.HTTP_200_OK)
