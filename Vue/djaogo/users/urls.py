from django.urls import path

from users import views

urlpatterns = [
    path('user/', views.user),
    path('users/', views.UserView.as_view()),
    path('users/<str:id>/', views.UserView.as_view()),
    path('api_users/', views.UserAPIView.as_view()),
    path('api_users/<str:id>/', views.UserAPIView.as_view()),
]
