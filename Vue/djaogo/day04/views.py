from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets

from day04.models import BookUser
from day04.serializers import BookModelSerializer
from utils.response import APIResponse


class UserLoginView(viewsets.ViewSet):

    #用户登陆逻辑
    def user_login(self, request, *args, **kwargs):
        try:
            #TODO post数据检测
            # user_ser = BookModelSerializer(data=request.data, many=True)
            # user_ser.is_valid(raise_exception=True)
            #登陆验证
            user = request.data.get("username")
            pwd = request.data.get("password")
            quesy_obj = BookUser.objects.filter(username=user,password=pwd,is_delete=False)
            logic = quesy_obj.count()
            if logic == 1:
                return APIResponse(200, "登陆成功", results="{'username':%s}"%user)
            else:
                return APIResponse(404, "用户名或密码错误")
        except:
            return APIResponse(500, "登陆失败")


class UserRegisterView(viewsets.ModelViewSet):
    queryset =BookUser.objects.filter()
    serializer_class = BookModelSerializer
    lookup_field = "username"
    #用户注册逻辑
    def user_register(self, request, *args, **kwargs):
        try:
            user = request.data.get("username")
            if BookUser.objects.filter(username=user).count()==0:
                result = self.create(request, *args, **kwargs)
                return  APIResponse(200,"注册成功",results=result.data)
            else:
                return APIResponse(0, "注册用户名已存在")
        except:
            return APIResponse(500, "注册数据有误 ")
    #检查用户名是否注册过
    def user_check(self,request, *args, **kwargs):
        result = self.retrieve(request, *args, **kwargs)
        return APIResponse(0, "注册用户名已存在，", results=result.data)