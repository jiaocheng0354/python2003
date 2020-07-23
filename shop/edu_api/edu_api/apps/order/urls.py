
from django.urls import path

from order import views

urlpatterns = [
    path('creat/', views.OrderView.as_view(),),
    path('list/', views.OrderListView.as_view(),)
]