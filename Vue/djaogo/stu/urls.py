from django.urls import path

from stu import views

urlpatterns = [
    path('api_stu/', views.StuAPIView.as_view()),
    path('api_stu/<str:id>/', views.StuAPIView.as_view()),
]
