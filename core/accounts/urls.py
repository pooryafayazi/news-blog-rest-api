from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    path("", include("django.contrib.auth.urls")),
    path("api/v1/", include("accounts.api.v1.urls")),    

    path('login/', views.login_view ,name='login'),
    path('logout', views.logout_view ,name='logout'),
    path('signup', views.signup_view ,name='signup'),  
]
