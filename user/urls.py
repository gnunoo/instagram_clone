from django.urls import path
from .views import Join,Login
urlpatterns = [
    path('login',Login.as_view()),
    path('join',Join.as_view()),

]
