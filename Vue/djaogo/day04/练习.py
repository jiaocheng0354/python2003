from rest_framework import generics
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin, RetrieveModelMixin, CreateModelMixin, UpdateModelMixin, \
    DestroyModelMixin
from rest_framework.views import APIView

from day04.models import BookUser
from day04.serializers import BookModelSerializer
from utils.response import APIResponse


class BookUserAPIView(APIView):
    def get(self, request, *args, **kwargs):
        user_list = BookUser.objects.filter(is_delete=False)
        result = BookModelSerializer(user_list,many=True).data
        return APIResponse(results=result)
class  BookUserGenericAPIView(ListModelMixin,
                         RetrieveModelMixin,
                         CreateModelMixin,
                         UpdateModelMixin,
                         DestroyModelMixin,
                         GenericAPIView):
    querset = BookUser.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "id"

    def get(self, request, *args, **kwargs):
        if "id" in kwargs:
            return  self.retrieve(request,*args, **kwargs)
        else:
            return  self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        response = self.update(request, *args, **kwargs)
        return APIResponse(results = response.data)
    def patch(self,request, *args, **kwargs):
        response = self.partial_update(request, *args, **kwargs)
        return APIResponse(results=response.data)
    def delete(self,request,*args, **kwargs):
        self.destroy(request, *args, **kwargs)
        return APIResponse(204)

class BookUserListAPIView(generics.ListCreateAPIView,generics.DestroyAPIView):
    queryset = BookUser.objects.filter(is_delete=False)
    serializer_class = BookModelSerializer
    lookup_field = "pk"

    def login(self, request, *args, **kwargs):
        pass
    def register(self, request, *arge, **kwargs):
        pass