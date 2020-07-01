from django.urls import path

from day04 import views

urlpatterns = [
    path('login/', views.UserLoginView.as_view({"post":"user_login"})),
    path('register/', views.UserRegisterView.as_view({"post":"user_register"})),
    path('register/<str:username>/', views.UserRegisterView.as_view({"get": "user_check"})),
]
