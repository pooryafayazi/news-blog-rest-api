from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.core import exceptions

from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
import random
from django.core.cache import cache

from ...models import User, Profile
from django.core.mail import send_mail



"""create JWT tokens for user"""
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        validated_data = super().validate(attrs)
        if not self.user.is_verified:
            raise serializers.ValidationError({"details": "user is not verified"})
        validated_data["email"] = self.user.email
        validated_data["user_id"] = self.user.id
        return validated_data



class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(username=email, password=password)
            if user is None:
                raise serializers.ValidationError('Invalid credentials')
        else:
            raise serializers.ValidationError('Must include "email" and "password"')

        attrs['user'] = user
        return attrs
    

class SignupSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    password1 = serializers.CharField(write_only=True, label="تکرار رمز عبور")
    first_name = serializers.CharField(write_only=True)
    last_name = serializers.CharField(write_only=True)    

    
    class Meta:
        model = User
        fields = ['email', 'password','password1', 'first_name', 'last_name']
        
    def validate(self, attrs):
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError({"email": "این ایمیل قبلاً ثبت‌نام شده است."})        

        if attrs['password'] != attrs['password1']:
            raise serializers.ValidationError({"password": "رمز عبور و تکرار آن برابر نیست."})
        
        return attrs

    def create(self, validated_data):
        validated_data.pop('password1')
        first_name = validated_data.pop('first_name')
        last_name = validated_data.pop('last_name')

        user = User.objects.create_user(**validated_data)

        # Profile.objects.create(user=user, first_name=first_name, last_name=last_name)

        profile = Profile.objects.get(user=user, pk=user.pk)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.save()

        code = random.randint(100000, 999999)
        cache.set(user.email, code, timeout=300)

        send_mail(
            'کد تأیید ایمیل',
            f'کد تأیید ایمیل شما: {code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )

        return user
    
    

class EmailVerificationSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email did not registered.")
        return value
    

    
class PasswordResetRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email is not registered.")
        return value

    def create(self, validated_data):
        email = validated_data['email']
        code = random.randint(100000, 999999)
        cache.set(email, code, timeout=180)

        send_mail(
            'Password Reset Code',
            f'Your password reset code is {code}',
            'from@example.com',
            [email],
            fail_silently=False,
        )

        return validated_data

    

class PasswordResetConfirmSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.IntegerField()
    new_password = serializers.CharField(write_only=True)
    new_password1 = serializers.CharField(write_only=True)

    def validate(self, attrs):
        if attrs.get("new_password") != attrs.get("new_password1"):
            raise serializers.ValidationError({"detail": "password dose not match"})
        email = attrs.get('email')
        code = attrs.get('code')
        
        cached_code = cache.get(email)
        if cached_code != code:
            raise serializers.ValidationError("Invalid or expired code.")
        return attrs
        # return super().validate(attrs)

    def save(self, **kwargs):
        email = self.validated_data['email']
        # new_password = self.validated_data['new_password']
        user = User.objects.get(email=email)
        # user.set_password(new_password)
        user.set_password(self.validated_data['new_password'])
        user.save()