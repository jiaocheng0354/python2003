# Create your views here.
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import ListModelMixin


from home.models import Banner, Nav
from home.response import APIResponse
from home.serializer import BannerModelSerializer, NavModelSerializer


class HomeBannerView(GenericAPIView, ListModelMixin):
    queryset = Banner.objects.filter()
    serializer_class = BannerModelSerializer

    def get(self, request, *args, **kwargs):
        results = self.list(request, *args, **kwargs)
        return APIResponse(200, True, results=results.data)


class HomeNavView(GenericAPIView, ListModelMixin, ):
    queryset = Nav.objects.filter()
    serializer_class = NavModelSerializer

    # lookup_field = "id"

    def get(self, request, *args, **kwargs):
        results = self.list(request, *args, **kwargs)
        return APIResponse(200, True, results=results.data)

