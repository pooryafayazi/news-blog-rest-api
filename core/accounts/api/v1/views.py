from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail

# from django.core.mail import send_mail
# from mail_templated import send_mail

# import jwt
# from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

# from datetime import datetime
# import datetime
# import pytz

from . import serializers
    
# from ..utils import EmailThread
from ...models import Profile


# from ...models import User

User = get_user_model()
from django.views.generic import TemplateView
# from django.shortcuts import render, redirect
from rest_framework import generics
from rest_framework_simplejwt.tokens import RefreshToken
# from django.contrib.auth import authenticate
from .serializers import LoginSerializer


"""create JWT tokens for user"""
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = serializers.CustomTokenObtainPairSerializer
    
    
    
# class LoginApiView(generics.GenericAPIView, TemplateView):
class LoginApiView(generics.GenericAPIView):
    serializer_class = serializers.LoginSerializer
    # template_name = 'accounts/login-api.html'

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token = self.get_tokens_for_user(user)
            return Response({'access': token, 'email': user.email}, status=200)

        return Response({'errors': serializer.errors}, status=400)

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)
    
    
    
class SignupView(generics.CreateAPIView):
    serializer_class = serializers.SignupSerializer

class EmailVerificationRequestView(generics.CreateAPIView):
    serializer_class = serializers.EmailVerificationSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        # Resend verification code
        code = cache.get(email)
        if code is None:
            code = random.randint(100000, 999999)
            cache.set(email, code, timeout=300)  # Store in cache for 5 minutes

            send_mail(
                'Verification email code',
                f'Your verification email code is : {code}',
                'from@example.com',
                [email],
                fail_silently=False,
            )

        return Response({"detail": "Verification code sent."}, status=status.HTTP_200_OK)
    
class VerifiedApiView(generics.GenericAPIView):
    serializer_class = serializers.VerifiedSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()  # This will update the user's verification status

        return Response({"detail": "Account verified successfully."}, status=status.HTTP_200_OK)
    
    
# class PasswordResetRequestView(generics.CreateAPIView, TemplateView):
class PasswordResetRequestView(generics.CreateAPIView, TemplateView):
    serializer_class = serializers.PasswordResetRequestSerializer
    # template_name = 'accounts/password_reset_request.html'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"detail": "Password reset code sent."}, status=status.HTTP_200_OK)
    

# class PasswordResetConfirmView(generics.UpdateAPIView, TemplateView):
class PasswordResetConfirmView(generics.UpdateAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    # template_name = 'accounts/password_reset_confirmation.html'

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save() 
        return Response({"detail": "Password has been reset successfully."}, status=status.HTTP_200_OK)
    


class ProfileApiView(generics.RetrieveUpdateAPIView):
    serializer_class = serializers.ProfileSerializer
    queryset = Profile.objects.all()
    
    def get_object(self):
        if self.request.user.is_anonymous:
            return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        queryset = self.get_queryset()
        obj = get_object_or_404(queryset, user=self.request.user)
        return obj

