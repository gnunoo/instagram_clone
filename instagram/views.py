from django.shortcuts import render
from rest_framework.views import APIView


class Sub(APIView):
    def get(self,request):
        print("get 호출")
        return render(request,'instagram/main.html')

    def post(self,request):
        print("post 호출")
        return render(request,'instagram/main.html')

# def test(request):
#     return render(request,'instagram/main.html')