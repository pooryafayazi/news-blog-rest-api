from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# from rest_framework.authtoken.views import ObtainAuthToken
app_name = "accounts-api-v1"

schema_view = get_schema_view(
    openapi.Info(
        title="Task API",
        default_version="v1",
        description="The description of ToDo CBV project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="poorya189@gmail.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # login jwt
    path("jwt/create/", views.CustomTokenObtainPairView.as_view(), name="jwt-create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="jwt-refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="jwt-verify"),
    
    # swagger
    path("swagger/", schema_view.with_ui("swagger", cache_timeout=0), name="schema-swagger-ui",),
    path("swagger/output.json", schema_view.without_ui(cache_timeout=0), name="schema-json",),
    
    # login signup forget password reset password
    path("login-api/", views.LoginApiView.as_view(), name="login-api"),
    path('password-reset-request-api/', views.PasswordResetRequestView.as_view(), name='password-reset-request-api'),
    path('password-reset-confirm-api/', views.PasswordResetConfirmView.as_view(), name='password-reset-confirm-api'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    # path('verify-email/', views.VerifyEmailView.as_view(), name='verify-email'),
    path('send-verification-code/', views.EmailVerificationRequestView.as_view(), name='send-verification-code'),
    
]
