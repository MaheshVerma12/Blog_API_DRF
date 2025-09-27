from django.contrib import admin
from django.urls import path
from home.views import *

urlpatterns = [
    path('blog/',BlogView.as_view()),
    path('public-blog/',PublicBlog.as_view())
    
]