import re

from django.contrib.auth.hashers import make_password
from django_redis import get_redis_connection
from rest_framework import serializers

from user.models import User


class UserModelSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=512, read_only=True, help_text="token")
    code = serializers.CharField(max_length=10, write_only=True, help_text="code")

    class Meta:
        model = User
        fields = ("id", "username", "password", "phone", "token", "code")
        extra_kwargs = {
            "id": {
                'read_only': True,
            },
            "username": {
                "read_only": True,
            },
            "password": {
                "write_only": True,
            },
            "phone": {
                "write_only": True
            }
        }

    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")
        code = attrs.get("code")
        # print(code)
        # 验证手机号格式
        if not re.match(r'^1[3-9]\d{9}$', phone):
            raise serializers.ValidationError("手机号格式错误")
        # 验证短信验证码
        redis_connection = get_redis_connection("sms_code")  # 获取redis连接
        sms_code = redis_connection.get("%s_check" % phone)
        # print(sms_code.decode())
        if sms_code is NameError:
            raise serializers.ValidationError("验证码失效")
        if code != sms_code.decode():
            raise serializers.ValidationError("验证码错误")
        return attrs

    def create(self, validated_data):
        pwd = validated_data.get("password")
        hash_password = make_password(pwd)
        username = validated_data.get("phone")

        # 添加数据
        user = User.objects.create(
            phone=username,
            username=username,
            password=hash_password,
        )

        # token
        from rest_framework_jwt.settings import api_settings
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(user)
        user.token = jwt_encode_handler(payload)
        return user
