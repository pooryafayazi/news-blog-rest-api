from django.urls import path, include

from . import views

app_name = "accounts"

urlpatterns = [
    # path("", include("django.contrib.auth.urls")),
    path("api/v1/", include("accounts.api.v1.urls")),
    
]