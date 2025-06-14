from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth import authenticate
from django.conf import settings
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .utils import send_normal_email
from .models import User

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)
    role = serializers.CharField(max_length=10, read_only=True) 

    class Meta:
        model = User
        fields = ['email', 'password', 'full_name', 'access_token', 'refresh_token', 'role']
    
    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        def get_user_role(user):
            if user.is_superuser:
                return 'admin'
            elif user.is_staff:
                return 'staff'
            else:
                return 'customer'
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed('invalid credential try again')
        if not user.is_active:
            raise AuthenticationFailed('User account locked')
        
        if hasattr(user, 'is_verified') and not user.is_verified:
            user.is_verified = True
            user.save(update_fields=['is_verified'])

        tokens = RefreshToken.for_user(user)
        return {
            'email': user.email,
            'full_name': user.get_full_name,
            'role':get_user_role(user),
            'access_token': str(tokens.access_token),
            'refresh_token': str(tokens)
        }

class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    default_error_message = {
        'bad_token': ('Token is expired or invalid')
    }

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('bad_token')
        
class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=68, write_only=True, required=True)
    new_password = serializers.CharField(max_length=68, write_only=True, required=True)
    confirm_new_password = serializers.CharField(max_length=68, write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New password does not match."})
        return super().validate(attrs)
    
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Old password is incorrect.")
        
        return value

    def save(self, **kwargs):
        user = self.context['request'].user
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("No user found with this email address.")
        return value
    
    def save(self):
        email = self.validated_data['email']
        user = User.objects.get(email=email)
        
        token_generator = PasswordResetTokenGenerator()
        token = token_generator.make_token(user)
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        
        frontend_url = settings.FRONTEND_URL

        reset_link = f"{frontend_url}/password-reset-confirm/{uidb64}/{token}/"
        
        email_subject = "Password reset request"
        email_body = f"Hi {user.first_name},\n\nPlease click the link below to reset your password:\n{reset_link}\n\nBest regards!"
        
        email_data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': email_subject
        }
        send_normal_email(email_data)   
        return self.validated_data


class SetNewPasswordSerializer(serializers.Serializer):
    new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    confirm_new_password = serializers.CharField(max_length=128, write_only=True, required=True)
    uidb64 = serializers.CharField(write_only=True, required=True)
    token = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['confirm_new_password']:
            raise serializers.ValidationError({"new_password": "New password does not match."})
            
        try:
            user_id = force_str(urlsafe_base64_decode(attrs['uidb64']))
            user = User.objects.get(id=user_id)

            token_generator = PasswordResetTokenGenerator()
            if not token_generator.check_token(user, attrs['token']):
                raise AuthenticationFailed('The password reset link is invalid or has expired.', 401)
            
            self.context['user'] = user
        
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise AuthenticationFailed('The password reset link is invalid or has expired.', 401)
        return super().validate(attrs)

    def save(self, **kwargs):
        user = self.context['user']
        user.set_password(self.validated_data['new_password'])
        user.save()
        return user
