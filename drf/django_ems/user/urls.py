from django.urls import path
from user import views

urlpatterns = [
    path('', views.UserView.as_view()),
    path('login/', views.UserLoginView.as_view({"post": "login"})),
    path('<str:username>/', views.UserView.as_view()),

]
