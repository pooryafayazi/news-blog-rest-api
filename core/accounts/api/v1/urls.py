from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

# from rest_framework.authtoken.views import ObtainAuthToken
app_name = "api-v1"

urlpatterns = [
    # login jwt
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),   
    
    
    # login signup forget password reset password
    path("login/", views.LoginApiView.as_view(), name="login-api"),
    path("verified/", views.VerifiedApiView.as_view(), name="Verified"),
    path('password-reset-request/', views.PasswordResetRequestView.as_view(), name='password-reset-request-api'),
    path('password-reset-confirm/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm-api'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    # path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('send-verification-code/', views.EmailVerificationRequestView.as_view(), name='send-verification-code'),
    
]
