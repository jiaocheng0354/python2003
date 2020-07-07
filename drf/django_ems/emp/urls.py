from django.urls import path

from emp import views

urlpatterns = [
    path('', views.EmpView.as_view()),
    path('list/', views.EmpListView.as_view()),
    path('<str:id>/', views.EmpView.as_view()),
]
