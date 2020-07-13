from django.urls import path
from rest_framework_jwt.views import ObtainJSONWebToken

from user import views

urlpatterns = [
    path("login/", ObtainJSONWebToken.as_view()),
    path("register/", views.UserAPIView.as_view()),
    path("verify/<str:phone>/", views.UserPhoneAPIView.as_view()),
    path("sms/<str:phone>/", views.SendMessageAPIView.as_view()),
    path("captcha/", views.CaptchaAPIView.as_view()),
    # path("captcha/<str:username>/", views.CaptchaAPIView.as_view()),
]
