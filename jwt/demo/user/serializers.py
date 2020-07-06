import re

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_jwt.settings import api_settings

from user.models import User

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class UserModelSerializer(ModelSerializer):
    login_name = serializers.CharField(write_only=True)
    pwd = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["login_name", "pwd", "username", "phone"]
        extra_kwargs = {
            "username": {
                "read_only": True,
            },
            "phone": {
                "read_only": True,
            },
        }

        def validate(self, attrs):
            login_name = attrs.get("login_name")
            pwd = attrs.get("pwd")

            if re.match(r'1[3-9][0-9]{9}', login_name):
                result = User.objects.filter(phone=login_name).first()
            else:
                result = User.objects.filter(username=login_name).first()

            if result and result.chectk_password(pwd):
                payload = jwt_payload_handler(result)
                token = jwt_encode_handler(payload)
                print(token)
                self.token = token
                self.obj = result
                print(attrs)
            return attrs
