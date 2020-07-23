# Create your views here.
import random
import re

from django_redis import get_redis_connection
from rest_framework.generics import CreateAPIView, GenericAPIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView

from edu_api.libs.geetest import GeetestLib
from edu_api.libs.sendsms import Message
from edu_api.utils.response import APIResponse
from user.models import User
from user.serializer import UserModelSerializer
from user.utils import get_user_by_account

pc_geetest_id = "6f91b3d2afe94ed29da03c14988fb4ef"
pc_geetest_key = "7a01b1933685931ef5eaf5dabefd3df2"


class CaptchaAPIView(APIView):
    # 验证码验证
    user_id = 0
    status = False

    def get(self, request, *args, **kwargs):
        username = request.query_params.get('username')
        user = get_user_by_account(username)
        if user is None:
            return APIResponse(400, False, results="用户不存在")
        self.user_id = user.id
        print(user.id)
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        self.status = gt.pre_process(self.user_id)
        # request.session[gt.GT_STATUS_SESSION_KEY] = status
        # request.session["user_id"] = user_id
        response_str = gt.get_response_str()
        # return APIResponse("success", True, results=response_str)
        return Response(response_str)

    def post(self, request, *args, **kwargs):
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        # status = request.session[gt.GT_STATUS_SESSION_KEY]
        # user_id = request.session["user_id"]
        if self.user_id:
            result = gt.success_validate(challenge, validate, seccode, self.user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        print(result)
        result = "true" if result else "false"
        return APIResponse(200, True, results=result)


# 注册用户
class UserAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserPhoneAPIView(GenericAPIView, RetrieveModelMixin):
    # 查询手机号是否存在
    queryset = User.objects.filter()
    serializer_class = UserModelSerializer
    lookup_field = "phone"

    def get(self, request, *args, **kwargs):
        results = self.retrieve(request, *args, **kwargs)
        return APIResponse(200, True, results=results.data)


class SendMessageAPIView(APIView):

    def get(self, request, *args, **kwargs):
        # 属性
        phone = kwargs.get("phone")
        API_KEY = "a19280256a714bad71b4b6cceb13a980"
        code = "%04d" % random.randint(0, 9999)
        redis_connection = get_redis_connection("sms_code")  # 获取redis连接

        # 判断号码有效性
        if not re.match(r"^1[3-9]\d{9}", phone):
            return APIResponse(400, False, results="手机号格式不正确")
        user = get_user_by_account(phone)
        # if user is not None:
        #     return APIResponse(400, False, results="手机号已经被注册")

        # 发送条件判断
        phone_code = redis_connection.get("%s_sms" % phone)
        phone_count = redis_connection.get("%s_count" % phone)
        if phone_code is not None:
            return APIResponse(300, False, results="%s已经在60s内发送过短息" % phone)
        else:
            redis_connection.setex("%s_sms" % phone, 60, code)
        if phone_count is None:
            redis_connection.setex("%s_count" % phone, 10 * 60, 1)
        else:
            redis_connection.incr("%s_count" % phone)
            if int(phone_count) > 3:
                return APIResponse(400, False, results="%s已经发送了三次，暂停发送" % phone)
        redis_connection.setex("%s_check" % phone, 10 * 60, code)  # 验证码的有效时间
        # 发短信
        try:
            message = Message(API_KEY)
            message.send_message(phone, code)
            # from my_task import send_sms
            # send_sms.delay(phone, code)
            print(phone, code)
        except:
            return APIResponse(500, False, results="短信发送失败")
        return APIResponse(200, False, results="短信发送成功")
