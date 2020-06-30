from rest_framework import serializers,exceptions

from library.models import Book

class BookModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ("book_name","price","img","publisher")
        extra_kwargs = {
            "book_name":{
                "required":True,
                "min_length":1,
                "error_messages":{
                    "required":"书名必填",
                    "min_length":"书名没实际意义"
                }
            },
            "publisher":{
                "write_only":True
            },
            "img":{
                "read_only":True
            }
        }
        def validate_book(self,value):
            if "@" in value:
                raise exceptions.ValidationError("书名输入有问题 ")
            return value
        # def validate(self,attrs):
        #     book_name = attrs.get("book_name")
        #     if book_name:
        #         raise exceptions.ValidationError("书名不能为空值 ")
        #     return attrs