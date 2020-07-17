# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from course.models import Course
from edu_api.settings import constants


class CartListView(ViewSet):
    user_id = 25

    # permission_classes = [IsAuthenticated]

    def cart_select(self, request):
        try:
            user_id = self.user_id
            course_id = request.data.get("course_id")
            select = request.data.get("select")
            print(course_id, select)
            redis_connection = get_redis_connection("cart")
            if course_id > 0:
                if select:
                    redis_connection.sadd("%s_selected" % user_id, course_id)
                else:
                    redis_connection.srem("%s_selected" % user_id, course_id)
                return Response("ok")
            elif (course_id == 0):
                key_list = redis_connection.hkeys("%s_cart" % user_id)
                for key in key_list:
                    redis_connection.sadd("%s_selected" % user_id, int(key))
                data = self.cart_show(user_id)
                return Response(data)
            return Response("null")
        except:
            return Response("error")

    def cart_del(self, request):
        user_id = self.user_id
        course_id = request.data.get("course_id")
        redis_connection = get_redis_connection("cart")
        pipeline = redis_connection.pipeline()
        if course_id>0:
            pipeline.multi()
            pipeline.hdel("%s_cart" % user_id, course_id)
            pipeline.srem("%s_selected" % user_id, course_id)
            pipeline.execute()
            course_len = redis_connection.hlen("%s_cart" % user_id)
        elif course_id==0:
            cart_key = redis_connection.hkeys("%s_cart" % user_id)
            for key in cart_key:
                course_id = int(key)
                print(course_id)
                # if redis_connection.hexists("%s_selected" % user_id, course_id ):
                pipeline.multi()
                pipeline.hdel("%s_cart" % user_id, course_id)
                pipeline.srem("%s_selected" % user_id, course_id)
                pipeline.execute()
            data = self.cart_show(user_id)
            return Response(data)
        return Response({"cart_length": course_len})

    def cart_list(self, request):
        user_id = self.user_id
        data = self.cart_show(user_id)
        return Response(data)

    def cart_update(self, request):

        course_id = request.data.get("course_id")
        # user_id = request.user.id
        user_id = self.user_id
        select = True
        expire = 0
        print(course_id)
        # 检测用户存在 todo
        try:
            Course.objects.get(is_show=True, is_delete=False, id=course_id)
        except:
            return Response({"message": "课程参数有误"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            redis_connection = get_redis_connection("cart")
            pipeline = redis_connection.pipeline()
            pipeline.multi()
            pipeline.hset("%s_cart" % user_id, course_id, expire)
            pipeline.sadd("%s_selected" % user_id, course_id)
            pipeline.execute()
            course_len = redis_connection.hlen("%s_cart" % user_id)
        except:
            return Response({"参数有误"})
        return Response({"message": "购物车添加成功", "cart_length": course_len})


    def cart_show(self,user_id):
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall('%s_cart' % user_id)
        select_list_bytes = redis_connection.smembers("%s_selected" % user_id)
        data = []
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            data.append({
                "selected": True if course_id_byte in select_list_bytes else False,
                "course_img": constants.IMAGE_SRC + course.course_img.url,
                "name": course.name,
                "id": course.id,
                "expire_id": expire_id,
                "price": course.price
                # "expire_list": course.expire_list,
                # "real_price": course.real_expire_price(expire_id),
            })
        return data