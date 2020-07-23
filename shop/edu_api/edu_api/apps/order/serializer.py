import random
from datetime import datetime

from django.db import transaction
from django_redis import get_redis_connection
from rest_framework import serializers, exceptions

from course.models import Course
from order.models import Order, OrderDetail

class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_number","pay_time","order_datail_list")

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id", "order_number", "pay_type",)
        extra_kwargs = {
            "id": {'read_only': True, },
            "order_number": {'read_only': True, },
            "pay_type": {'write_only': True, },
        }

    def validate(self, attrs):
        pay_type = attrs.get("pay_type")
        try:
            Order.pay_choices[pay_type]
        except Order.DoesNotExist:
            raise serializers.ValidationError("支付方法无效")
        return attrs

    def create(self, validated_data):
        user_id = 25
        user_id1 = self.context["request"].user.id
        print(user_id1,"aaa")
        pay_type = validated_data.get("pay_type")
        redis_connection = get_redis_connection("cart")
        cart_list_bytes = redis_connection.hgetall('%s_cart' % user_id)
        select_list_bytes = redis_connection.smembers("%s_selected" % user_id)
        # 计算出总价
        real_price = 0  # 实付金额
        total_price = 0  # 订单总价
        count = 0
        for course_id_byte in select_list_bytes:
            course_id = int(course_id_byte)
            for course_id_byte, expire_id_byte in cart_list_bytes.items():
                course_id_cart = int(course_id_byte)
                if course_id == course_id_cart:
                    try:
                        course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                        expire_id = int(expire_id_byte)
                        real_price += float(course.real_expire_price(expire_id))
                        price = "%.2f" % course.price
                        total_price += float(price)
                        count += 1
                    except Course.DoesNotExist:
                        continue
        if count == 0:
            raise serializers.ValidationError("订单无效")
        # 订单号
        order_number = datetime.now().strftime("%Y%m%d%H%M%S") + "%06d" % user_id + "%06d" % random.randint(0, 999999)
        # 事务开启
        with transaction.atomic():
            # 记录下事务回滚的点
            rollback_id = transaction.savepoint()
            # 生成订单
            try:
                order = Order.objects.create(order_title="课程订单", total_price=total_price, real_price=real_price,
                                             order_number=order_number, order_status=0, pay_type=pay_type, credit=0,
                                             coupon=0, order_desc="订单描述", user_id=user_id)
            except:
                transaction.savepoint_rollback(rollback_id)
                raise serializers.ValidationError("订单生成失败")

            for course_id_byte, expire_id_byte in cart_list_bytes.items():
                course_id = int(course_id_byte)
                expire_id = int(expire_id_byte)
                try:
                    course = Course.objects.get(is_show=True, is_delete=False, pk=course_id)
                except Course.DoesNotExist:
                    continue
                else:
                    if course_id_byte in select_list_bytes:
                        try:
                            order_detail = OrderDetail.objects.create(
                                order=order,
                                course=course,
                                expire=expire_id,
                                price=course.price,
                                real_price=course.real_expire_price(expire_id),
                                discount_name=course.discount_name
                            )
                        # order_detail.save()
                        except:
                            transaction.savepoint_rollback(rollback_id)
                            raise serializers.ValidationError("订单生成失败")
            order.save()
        # 删除购物车下定单记录
        cart_key = redis_connection.smembers("%s_selected" % user_id)
        pipeline = redis_connection.pipeline()
        for key in cart_key:
            course_id = int(key)
            print(course_id)
            pipeline.multi()
            pipeline.hdel("%s_cart" % user_id, course_id)
            pipeline.srem("%s_selected" % user_id, course_id)
            pipeline.execute()

        return order
