from rest_framework import serializers,exceptions

from day04.models import BookUser


class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookUser
        fields = ("username","password","maill","tel")
        extra_kwargs = {
            "username":{
                "required":True,
                "min_length":20,
                "error_messages":{
                    "required":"用户名必填",
                    "min_length":"用户名太短了"
                }
            },
            "password":{
                "write_only":True
            },
            "maill": {
                "write_only": True
            },
            "tel": {
                "write_only": True
            }
        }
        def validate_username(self,value):
            if "1" in value:
                raise exceptions.ValidationError("用户名输入有问题 ")
            return value
        def validate(self,attrs):
            username = attrs.get("username")
            if username=="admin":
                raise exceptions.ValidationError("用户名不能为空值 ")
            return attrs