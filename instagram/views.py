import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from main.settings import MEDIA_ROOT
from .models import Feed
from user.views import User

class Main(APIView):
    def get(self,request):
        print("get 호출")

        feed_list=Feed.objects.all().order_by('-id')


        email=request.session.get('email',None)

        if email is None:
            return render(request,"user/login.html")
        #일치하는 이메일 유저 정보 가져오기(1개)
        user=User.objects.filter(email=email).first()

        if user is None:
            return render(request,"user/login.html")
        return render(request,'instagram/main.html',context=dict(feed_list=feed_list, user=user))



class UploadFeed(APIView):

    def post(self,request):
        print('post 호출')
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

        image=uuid_name
        content=request.data.get('content')
        user_id=request.data.get('user_id')
        profile_image=request.data.get('profile_image')

        Feed.objects.create(content=content, Feed_image=image, profile_image=profile_image, user_id=user_id, like_count=0)

        return Response(status=200)

