from django.shortcuts import render
from rest_framework.views import APIView

from instagram.models import Feed, Like, Bookmark
from user.models import User


class Profile(APIView):

    def get(self, request):
        email = request.session.get('email', None)

        if email is None:
            return render(request, "user/login.html")
        # 일치하는 이메일 유저 정보 가져오기(1개)
        user = User.objects.filter(email=email).first()

        if user is None:
            return render(request, "user/login.html")

        feed_list=Feed.objects.filter(email=email).all()
        like_list=list(Like.objects.filter(email=email,is_like=True).values_list('feed_id',flat=True))
        like_feed_list=Feed.objects.filter(id__in=like_list)
        bookmark_list=list(Bookmark.objects.filter(email=email,is_marked=True).values_list('feed_id',flat=True))
        bookmark_feed_list=Feed.objects.filter(id__in=bookmark_list)

        return render(request, "content/profile.html", context=dict(feed_list=feed_list, like_feed_list=like_feed_list, bookmark_feed_list=bookmark_feed_list , user=user))