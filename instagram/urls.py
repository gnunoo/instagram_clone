from django.contrib import admin
from django.urls import path
from .views import Main,UploadFeed,UploadReplay,Toggllike,TogglBookmark

urlpatterns = [
    path('', Main.as_view()),
    path('reply', UploadReplay.as_view()),
    path('like', Toggllike.as_view()),
    path('bookmark',TogglBookmark.as_view())
]

