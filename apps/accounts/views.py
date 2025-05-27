from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .ratelimit import rate_limit_decorator
from .serializers import LoginSerializer, LogoutUserSerializer

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
