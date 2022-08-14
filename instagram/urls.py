from django.contrib import admin
from django.urls import path
from .views import Main,UploadFeed

urlpatterns = [
    path('', Main.as_view()),
    # path('content/uploadFeed', UploadFeed.as_view())
]

