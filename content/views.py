from django.shortcuts import render
from rest_framework.views import APIView

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

        return render(request, "content/profile.html", context=dict(user=user))