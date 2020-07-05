from django.shortcuts import render

# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import RetrieveModelMixin, CreateModelMixin, ListModelMixin
from rest_framework.viewsets import ViewSet

from user.models import User
from user.serializers import UserModelSerializer
from utils.response import APIResponse


class UserView(RetrieveModelMixin, CreateModelMixin, ListModelMixin, GenericAPIView):
    queryset = User.objects.filter()
    serializer_class = UserModelSerializer

    def get(self, request, *args, **kwargs):
        username = kwargs.get("username")
        if username:
            num = User.objects.filter(username=username).count()
            msg = True if num == 1 else False
            return APIResponse(200, msg, results=username)
        return APIResponse(400, False)

    def post(self, request, *args, **kwargs):
        result = self.create(request, *args, **kwargs)
        return APIResponse(200, True, results=result.data)


class UserLoginView(ViewSet):

    def login(self, request, *args, **kwargs):
        try:
            # 登陆验证
            user = request.data.get("username")
            pwd = request.data.get("password")
            print(user)
            quesy_obj = User.objects.filter(username=user, password=pwd)
            logic = quesy_obj.count()
            if logic == 1:
                return APIResponse(200, True, results="{'username':%s}" % user)
            else:
                return APIResponse(404, False)
        except:
            return APIResponse(500, False)
