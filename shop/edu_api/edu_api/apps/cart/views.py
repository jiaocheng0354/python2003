# Create your views here.
from django_redis import get_redis_connection
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework.request import Request

from course.models import Course, CourseExpire
from edu_api.settings import constants


class CartListView(ViewSet):
    user_id = 25

    # permission_classes = [IsAuthenticated]
    def cart_expire(self, request):
        try:
            user_id = self.user_id
            course_id = request.data.get("course_id")
            expire_id = request.data.get("expire_id")
            try:
                course = Course.objects.get(is_show=True, is_delete=False, id=course_id)
                if expire_id > 0:
                    expire_iem = CourseExpire.objects.filter(is_show=True, is_delete=False, id=expire_id)
                    if not expire_iem:
                        raise Course.DoesNotExist()
            except Course.DoesNotExist:
                return Response("课程信息不存在")

            real_price = course.real_expire_price(expire_id)

            redis_connection = get_redis_connection("cart")
            redis_connection.hset("%s_cart" % user_id, course_id, expire_id)
            cart_list_bytes = redis_connection.hgetall('%s_cart' % user_id)
            select_list_bytes = redis_connection.smembers("%s_selected" % user_id)
            count_num = 0
            for course_id_byte in select_list_bytes:
                course_id = int(course_id_byte)
                for course_id_byte, expire_id_byte in cart_list_bytes.items():
                    course_id_cart = int(course_id_byte)
                    if course_id == course_id_cart:
                        try:
                            course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                        except Course.DoesNotExist:
                            continue
                        expire_id = int(expire_id_byte)
                        count_num += float(course.real_expire_price(expire_id))
            count_price = "%.2f" % count_num
            return Response({"real_price": real_price, "count_price": count_price})
        except:
            return Response("error")

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
            elif (course_id == 0):
                if select:
                    key_list = redis_connection.hkeys("%s_cart" % user_id)
                    for key in key_list:
                        redis_connection.sadd("%s_selected" % user_id, int(key))
                else:
                    key_list = redis_connection.hkeys("%s_cart" % user_id)
                    for key in key_list:
                        redis_connection.srem("%s_selected" % user_id, int(key))
            data = self.cart_show(user_id)
            return Response(data)
        except:
            return Response("error")

    def cart_del(self, request):
        user_id = self.user_id
        course_id = request.data.get("course_id")
        redis_connection = get_redis_connection("cart")
        pipeline = redis_connection.pipeline()
        if course_id > 0:
            pipeline.multi()
            pipeline.hdel("%s_cart" % user_id, course_id)
            pipeline.srem("%s_selected" % user_id, course_id)
            pipeline.execute()
            course_len = redis_connection.hlen("%s_cart" % user_id)
        elif course_id == 0:
            cart_key = redis_connection.smembers("%s_selected" % user_id)
            for key in cart_key:
                course_id = int(key)
                print(course_id)
                pipeline.multi()
                pipeline.hdel("%s_cart" % user_id, course_id)
                pipeline.srem("%s_selected" % user_id, course_id)
                pipeline.execute()
        data = self.cart_show(user_id)
        return Response(data)

    def cart_list(self, request):
        print(request.user.id)
        user_id = self.user_id
        data = self.cart_show(user_id)
        # print(data)
        return Response(data)

    def cart_update(self, request):

        course_id = request.data.get("course_id")
        # user_id = request.user.id
        user_id = self.user_id
        select = True
        expire = 0
        # print(course_id)
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

    def cart_show(self, user_id):
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall('%s_cart' % user_id)
        select_list_bytes = redis_connection.smembers("%s_selected" % user_id)
        data = []
        count_price = 0
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
                "price": course.price,
                "expire_list": course.expire_list,
                "real_price": course.real_expire_price(expire_id),
            })
        for course_id_byte in select_list_bytes:
            course_id = int(course_id_byte)
            for course_id_byte, expire_id_byte in cart_list_bytes.items():
                course_id_cart = int(course_id_byte)
                if course_id == course_id_cart:
                    try:
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                    except Course.DoesNotExist:
                        continue
                    expire_id = int(expire_id_byte)
                    print(float(course.real_expire_price(expire_id)))
                    count_price += float(course.real_expire_price(expire_id))

        return data, "%.2f" % count_price

class OrderListView(ViewSet):
    user_id = 25

    def order_list(self, request):
        user_id = self.user_id
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall('%s_cart' % user_id)
        select_list_bytes = redis_connection.smembers("%s_selected" % user_id)
        data = []
        count_price = 0
        for course_id_byte, expire_id_byte in cart_list_bytes.items():
            course_id = int(course_id_byte)
            expire_id = int(expire_id_byte)
            try:
                course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
            except Course.DoesNotExist:
                continue
            if course_id_byte in select_list_bytes:
                data.append({
                    "course_img": constants.IMAGE_SRC + course.course_img.url,
                    "name": course.name,
                    "id": course.id,
                    "expire_id": expire_id,
                    "price": course.price,
                    "expire_list": course.expire_list,
                    "real_price": course.real_expire_price(expire_id),
                    "discount_name":course.discount_name,
                })
        for course_id_byte in select_list_bytes:
            course_id = int(course_id_byte)
            for course_id_byte, expire_id_byte in cart_list_bytes.items():
                course_id_cart = int(course_id_byte)
                if course_id == course_id_cart:
                    try:
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                    except Course.DoesNotExist:
                        continue
                    expire_id = int(expire_id_byte)
                    print(float(course.real_expire_price(expire_id)))
                    count_price += float(course.real_expire_price(expire_id))

        return Response({"order":data,"count_price": "%.2f" % count_price})