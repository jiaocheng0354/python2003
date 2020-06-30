# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from library.models import Book
from library.serializers import BookModelSerializer


class BookAPIView(APIView):
    def get(self,request,*args,**kwargs):
        id = kwargs.get("id")
        if id:
            book_query = Book.objects.filter(pk=id,is_delete=False)
            book_stringify = BookModelSerializer(book_query,many=True).data
            return Response({
                "statur":200,
                "message":"查询单个图书成功",
                "results": book_stringify
            })
        else:
            book_many = Book.objects.filter(is_delete=False)
            book_many_stringify = BookModelSerializer(book_many,many=True).data
            return Response({
                "statur":200,
                "message":"查询图书成功",
                "results":book_many_stringify
            })
    def post(self,request,*args,**kwargs):

        request_data = request.data
        if isinstance(request_data,dict):
            many = False
        elif isinstance(request_data,list):
            many = True
        else:
            return Response({
                "status":400,
                "message":"数据格式有误",
            })
        book_parse = BookModelSerializer(data=request_data,many=many)
        book_parse.is_valid(raise_exception=True)
        result = book_parse.save()
        return Response({
            "status":200,
            "message":"添加图书成功",
            "result":BookModelSerializer(result,many=many).data
        })
    def delete(self,request,*args,**kwargs):
        id = kwargs.get("id")
        print(request.data)
        if id:
            ids = [id]
        else:
            ids = request.data.get("ids")
        response = Book.objects.filter(pk__in=ids, is_delete=False).update(is_delete=True)
        if response:
            return Response({
                "status": 200,
                "message": "删除成功"
            })

        return Response({
            "status": 400,
            "message": "删除失败或图书不存在"
        })
    def put(self,request,*args,**kwargs):
        request_data = request.data
        id = kwargs.get("id")
        book_query = Book.objects.get(pk=id)
        # if ~book_query:
        #     return  Response({
        #         "starus":400,
        #         "message":"图书不存在"
        #     })
        book_stringify = BookModelSerializer(data=request_data,
                                             instance=book_query,partial=False)
        book_stringify.is_valid(raise_exception=True)
        result = book_stringify.save()
        return Response({
            "status":200,
            "message":"更新成功",
            "results":BookModelSerializer(result).data
        })
    def patch(self,request,*args,**kwargs):
        request_data = request.data
        id = kwargs.get("id")
        book_query = Book.objects.get(pk=id)
        # if ~book_query:
        #     return  Response({
        #         "starus":400,
        #         "message":"图书不存在"
        #     })
        book_stringify = BookModelSerializer(data=request_data,
                                             instance=book_query,partial=True)
        book_stringify.is_valid(raise_exception=True)
        result = book_stringify.save()
        return Response({
            "status":200,
            "message":"更新成功",
            "results":BookModelSerializer(result).data
        })