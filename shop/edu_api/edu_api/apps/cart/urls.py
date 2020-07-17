from django.urls import path

from cart import views

urlpatterns = [
    path('list/', views.CartListView.as_view(
        {"get": "cart_list", "post": "cart_update", "delete": "cart_del", "patch": "cart_select"})),
]
