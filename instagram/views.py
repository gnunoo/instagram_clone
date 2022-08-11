from django.shortcuts import render
from rest_framework.views import APIView
from .models import Feed

class Main(APIView):
    def get(self,request):
        print("get 호출")
        feed_list=Feed.objects.all().order_by('-id')


        return render(request,'instagram/main.html',context=dict(feed_list=feed_list))

    def post(self,request):
        print("post 호출")
        return render(request,'instagram/main.html')


