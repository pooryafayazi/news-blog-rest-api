from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView
from . import views


app_name = 'api-v1'

urlpatterns = []

# 4.2 viewsets.ModelViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register('posts', views.PostModelViewSet, basename='post')
router.register('categories', views.CategoryModelViewSet, basename='category')
router.register('comments', views.PostCommentModelViewSet, basename='comment')
urlpatterns += router.urls