from django.shortcuts import render

# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from user.jwtauthentication import JWTAuthentication
from user.serializers import UserModelSerializer
from utils.response import APIResponse


class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    def get(self,request, *args, **kwargs):
        return APIResponse(results={"username": request.user.username})

class LoginAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def post(self, request, *args, **kwargs):
        user_ser = UserModelSerializer(data=request.data)
        user_ser.is_valid(raise_exception=True)
        result = UserModelSerializer(user_ser).data
        # print(user_ser)
        return APIResponse(200,"ok", results=result)