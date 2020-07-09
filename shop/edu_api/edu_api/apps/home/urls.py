from django.urls import path

from home import views

urlpatterns = [
    path('banner/', views.HomeBannerView.as_view()),
    path('nav/', views.HomeNavView.as_view()),
]