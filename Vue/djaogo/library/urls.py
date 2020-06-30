from django.urls import path

from library import views

urlpatterns = [
    path('books/', views.BookAPIView.as_view()),
    path('books/<str:id>/', views.BookAPIView.as_view()),
]
