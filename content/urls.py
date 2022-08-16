from django.urls import path
from .views import Profile
from instagram.views import Main
urlpatterns = [
    path('profile', Profile.as_view()),
    path('main',Main.as_view())
]