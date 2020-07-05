from rest_framework import serializers,exceptions

from user.models import User

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('__all__')
        extra_kwargs = {
            "username":{
                "required":True,
                "min_length":2,
                "error_messages":{
                    "required":"用户名必填",
                    "min_length":"用户名太短了"
                }
            },
            "name":{
                "write_only":True
            },
            "password": {
                "write_only": True
            },
            "sex": {
                "write_only": True
            }
        }
        # def validate_username(self,value):
        #     if "@" in value:
        #         raise exceptions.ValidationError("用户名输入有问题 ")
        #     return value
        # def validate(self,attrs):
        #     username = attrs.get("username")
        #     if username=="admin":
        #         raise exceptions.ValidationError("用户名不能为空值 ")
        #     return attrs