# Create your views here.
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.mixins import ListModelMixin
from rest_framework.permissions import IsAuthenticated

from home.response import APIResponse
from order.models import Order
from order.serializer import OrderSerializer, OrderListSerializer


class OrderView(CreateAPIView):
    # permission_classes = [IsAuthenticated]
    queryset = Order.objects.filter()
    serializer_class = OrderSerializer

class OrderListView(ListAPIView):
    queryset = Order.objects.filter()
    serializer_class = OrderListSerializer

