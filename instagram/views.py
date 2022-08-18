import os
from uuid import uuid4
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from main.settings import MEDIA_ROOT
from .models import Feed, Reply, Like, Bookmark
from user.views import User

class Main(APIView):
    def get(self,request):

        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")
        # 일치하는 이메일 유저 정보 가져오기(1개)
        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")


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

            like_count=Like.objects.filter(feed_id=feed.id, is_like=True).count()
            is_liked=Like.objects.filter(feed_id=feed.id, email=email,is_like=True).exists()
            is_marked=Bookmark.objects.filter(feed_id=feed.id, email=email,is_marked=True).exists()

            feed_list.append(dict(
                id=feed.id,
                content=feed.content,
                Feed_image=feed.Feed_image,
                email=feed.email,
                like_count=like_count,
                profile_imag=user.profile_img,
                nickname=user.nickname,
                reply_list=reply_list,
                is_liked=is_liked,
                is_marked=is_marked
            ))


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

        Feed.objects.create(content=content, Feed_image=image, email=email)

        return Response(status=200)

class UploadReplay(APIView):
    def post(self,request):
        feed_id=request.data.get('feed_id',None)
        reply_content=request.data.get('reply_content',None)
        email = request.session.get('email',None)

        Reply.objects.create(feed_id=feed_id,reply_content=reply_content,email=email)

        return Response(status=200)

class Toggllike(APIView):
    def post(self,request):
        feed_id=request.data.get('feed_id',None)
        favorite_text=request.data.get('favorite_text',None)

        if favorite_text=='favorite_border':
            is_like=True
        else:
            is_like=False

        email = request.session.get('email',None)

        like=Like.objects.filter(feed_id=feed_id,email=email).first()
        if like:
            like.is_like=is_like
            like.save()
        else:
            Like.objects.create(feed_id=feed_id,is_like=is_like,email=email)

        return Response(status=200)



class TogglBookmark(APIView):
    def post(self,request):
        feed_id=request.data.get('feed_id',None)
        bookmark_text=request.data.get('bookmark_text',None)

        if bookmark_text=='bookmark_border':
            is_marked=True
        else:
            is_marked=False

        email = request.session.get('email',None)

        bookmark=Bookmark.objects.filter(feed_id=feed_id,email=email).first()
        if bookmark:
            bookmark.is_marked=is_marked
            bookmark.save()
        else:
            Bookmark.objects.create(feed_id=feed_id,is_marked=is_marked,email=email)

        return Response(status=200)