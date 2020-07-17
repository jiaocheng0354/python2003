from django.urls import path
from rest_framework_jwt.views import obtain_jwt_token

from user import views

urlpatterns = [
    path("login/", obtain_jwt_token),
    path("register/", views.UserAPIView.as_view()),
    path("verify/<str:phone>/", views.UserPhoneAPIView.as_view()),
    path("sms/<str:phone>/", views.SendMessageAPIView.as_view()),
    path("captcha/", views.CaptchaAPIView.as_view()),
]

