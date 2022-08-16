import os
from uuid import uuid4

from django.contrib.auth.hashers import make_password
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from main.settings import MEDIA_ROOT
from .models import User


class Join(APIView):
    def get(self, request):
        return render(request, "user/join.html")

    def post(self, request):
        email = request.data.get('email', None)
        nickname = request.data.get('nickname', None)
        name = request.data.get('name', None)
        password = request.data.get('password', None)

        User.objects.create(email=email,
                            nickname=nickname,
                            name=name,
                            password=make_password(password),
                            profile_img="default_profile.jpg")



        return Response(status=200)


class Login(APIView):

    def get(self, request):
        return render(request, "user/login.html")

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        # 일치하는 이메일 유저 정보 가져오기
        user=User.objects.filter(email=email).first()

        if user is None:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))

        if user.check_password(password):
            request.session['email']=email
            return Response(status=200)
        else:
            return Response(status=404, data=dict(message="회원정보가 잘못되었습니다."))


class Logout(APIView):

    def get(self, request):
        request.session.flush()
        return render(request, "user/login.html")


class UploadProfile(APIView):

    def post(self,request):

        #파일 불러오기
        file = request.FILES['file']
        #파일 이름 고유값으로 만들기
        uuid_name = uuid4().hex
        #base+media+uuid
        save_path = os.path.join(MEDIA_ROOT, uuid_name)
        #파일 쓰기
        with open(save_path, 'wb+') as destination:
            #파일 조각 내서 쓰기
            for chunk in file.chunks():
                destination.write(chunk)

        profile_image=uuid_name
        email=request.data.get('email')

        user=User.objects.filter(email=email).first()

        user.profile_img=profile_image
        user.save()


        return Response(status=200)