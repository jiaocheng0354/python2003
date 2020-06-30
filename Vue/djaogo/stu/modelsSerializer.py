from rest_framework import serializers

from stu.models import Stu


class StuSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=80)
    age = serializers.IntegerField()
    password = serializers.CharField(max_length=64)
    grade = serializers.CharField(max_length=10)
    stuNumber = serializers.IntegerField()


class StuDeSerializer(serializers.Serializer):
    username = serializers.CharField(min_length=1)
    age = serializers.IntegerField()
    password = serializers.CharField()
    grade = serializers.CharField()
    stuNumber = serializers.CharField(required=False)

    def create(self,validated_data):
        pass
        return Stu.objects.create(**validated_data)
