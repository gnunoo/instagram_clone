from django.contrib import admin
from django.urls import path
from .views import Main,UploadFeed,UploadReplay

urlpatterns = [
    path('', Main.as_view()),
    path('reply', UploadReplay.as_view())
]

