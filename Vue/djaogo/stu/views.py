# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from stu.models import Stu
from stu.modelsSerializer import StuSerializer, StuDeSerializer


class StuAPIView(APIView):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("id")
        if id:
            result = Stu.objects.get(pk=id)
            if result:
                return Response({
                    "status": 200,
                    "message": "查询单个同学成功",
                    "results": StuSerializer(result).data
                })
        else:
            user_list = Stu.objects.all()
            if user_list:
                return Response({
                    "status": 200,
                    "message": "查询所有同学成功",
                    "results": StuSerializer(user_list,many=True).data,
                })
        return Response({
            "status": 500,
            "message": "查询失败",
        })

    def post(self, request, *args, **kwargs):
        stu_data = request.data
        print(stu_data)
        try:
            if stu_data:
                stu_serializer = StuDeSerializer(data=stu_data)
                print(1)
                if stu_serializer.is_valid():
                    print(2)
                    result = stu_serializer.save()
                    print(3)
                    return Response({
                        "status": 201,
                        "message": "填加同学成功",
                        "results": StuSerializer(result).data,
                        # StuSerializer(result),
                    })
        except:
            return Response({
                "status": 500,
                "message": "填加同学失败",
                "results": serializer.errors,
            })