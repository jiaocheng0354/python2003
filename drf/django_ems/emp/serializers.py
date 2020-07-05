from rest_framework import serializers, exceptions

from emp.models import Emp


class EmpModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Emp
        fields = ("id", "name", "photo", "salary", "age")
        extra_kwargs = {
            "name": {
                "required": True,
                "min_length": 2,
                "error_messages": {
                    "required": "必填",
                    "min_length": "太短了"
                }
            },
            "age": {
                "max_value":120,
                "error_messages": {
                    "max_value": "年龄不可能超120"
                }
            }
        }

        # def validate_username(self, value):
        #     if "1" in value:
        #         raise exceptions.ValidationError(" ")
        #     return value
        #
        # def validate(self, attrs):
        #     name = attrs.get("username")
        #     if name == "admin":
        #         raise exceptions.ValidationError("")
        #     return attrs
