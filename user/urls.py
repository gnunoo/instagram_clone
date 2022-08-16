from django.urls import path
from .views import Join,Login,Logout,UploadProfile
urlpatterns = [
    path('login',Login.as_view()),
    path('join',Join.as_view()),
    path('logout',Logout.as_view()),
    path('profile/upload',UploadProfile.as_view())

]
