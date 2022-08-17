import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from main.settings import MEDIA_ROOT
from .models import Feed, Reply
from user.views import User

class Main(APIView):
    def get(self,request):
        print("get 호출")
        feed_object_list=Feed.objects.all().order_by('-id')
        feed_list=[]

        for feed in feed_object_list:
            user=User.objects.filter(email=feed.email).first()
            reply_object_list=Reply.objects.filter(feed_id=feed.id)
            reply_list=[]
            for reply in reply_object_list:
                user = User.objects.filter(email=reply.email).first()
                reply_list.append(dict(
                    feed_id=reply.feed_id,
                    reply_content=reply.reply_content,
                    nickname=user.nickname
                ))


            feed_list.append(dict(
                id=feed.id,
                content=feed.content,
                Feed_image=feed.Feed_image,
                like_count=feed.like_count,
                email=feed.email,
                profile_imag=user.profile_img,
                nickname=user.nickname,
                reply_list=reply_list,
            ))

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
        email=request.session.get('email')

        Feed.objects.create(content=content, Feed_image=image, email=email, like_count=0)

        return Response(status=200)

class UploadReplay(APIView):
    def post(self,request):
        feed_id=request.data.get('feed_id',None)
        reply_content=request.data.get('reply_content',None)
        email = request.session.get('email',None)

        Reply.objects.create(feed_id=feed_id,reply_content=reply_content,email=email)

        return Response(status=200)