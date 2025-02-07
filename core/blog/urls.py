from django.contrib import admin
from django.urls import path,include
from django.views.generic.base import RedirectView
from . import views


app_name = 'blog'

urlpatterns= [
    
    # redirect to a url
    # path('go-to-about/', RedirectView.as_view(url='http://www.itmeter.ir/about'), name='go-to-about'),
    # redirect to TemplateView
    # path('go-to-about/', RedirectView.as_view(pathern_name='blog:'), name='go-to-about'),
    
    
    path('api/v1/', include('blog.api.v1.urls'))
]