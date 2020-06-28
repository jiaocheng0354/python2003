from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

# Create your views here.
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView

from users.models import User


def user(request):
    pass
    return HttpResponse("user sucess")

@method_decorator(csrf_exempt,name="dispatch")
class UserView(View):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        if id:
            result = User.objects.filter(id=id).values()[0]
            if result:
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": result
                })
        else:
            user_list = User.objects.all().values()
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_list),
                })
        return  JsonResponse({
            "status":500,
            "message":"查询失败",
        })
    def post(self,request,*args,**kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        try:
            result = User.objects.create(username=username,password=password,gender=0)
            return JsonResponse({
                "status": 201,
                "message": "填加用户成功",
                "results": {"username":result.username,"gender":result.gender},
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "填加用户失败",
            })

        def put(self, request, *args, **kwargs):
            id = request.POST.get("id")
            username = request.POST.get("username")
            password = request.POST.get("password")
            gender = request.POST.get("gender")
            print(id,username,password,gender)
            try:
                result = User.objects.filter(id=int(id))
                result.username = username
                result.password = password
                result.gender = gender
                result.save()
                return JsonResponse({
                    "status": 200,
                    "message": " 修改用户成功",
                    "results": {"username":result.username,"gender":result.gender},
                })
            except:
                return JsonResponse({
                    "status": 500,
                    "message": " 修改用户失败",
                })

        def delete(self, request, *args, **kwargs):
            # request:  WSGIrequest
            print("DELETE SUCCESS  删除")
            return HttpResponse("DELETE SUCCESS")


class UserAPIView(APIView):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        if id:
            result = User.objects.filter(id=id).values()[0]
            if result:
                return JsonResponse({
                    "status": 200,
                    "message": "查询单个用户成功",
                    "results": result
                })
        else:
            user_list = User.objects.all().values()
            if user_list:
                return JsonResponse({
                    "status": 200,
                    "message": "查询所有用户成功",
                    "results": list(user_list),
                })
        return  JsonResponse({
            "status":500,
            "message":"查询失败",
        })
    def post(self,request,*args,**kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        print(username,password)
        try:
            result = User.objects.create(username=username,password=password,gender=0)
            return JsonResponse({
                "status": 201,
                "message": "填加用户成功",
                "results": {"username":result.username,"gender":result.gender},
            })
        except:
            return JsonResponse({
                "status": 500,
                "message": "填加用户失败",
            })