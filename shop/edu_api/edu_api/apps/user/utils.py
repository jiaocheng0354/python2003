import re

from django.contrib.auth.backends import ModelBackend

# jwt的返回值
from django.db.models import Q
from django_redis import get_redis_connection

from user.models import User


def jwt_response_payload_handler(token, user=None, request=None):
    return {
        'token': token,
        'username': user.username,
        "user_id": user.id
    }


def get_user_by_account(account):
    try:
        user = User.objects.filter(Q(username=account) | Q(phone=account)).first()
    except:
        return None
    else:
        return user


class UserAuthBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = get_user_by_account(username)
        print(re.match(r'^[0-9]{4}$', password))
        if not re.match(r'^[0-9]{4}$', password):
            if user and user.check_password(password) and user.is_authenticated:
                return user
            else:
                return None
        else:
            redis_connection = get_redis_connection("sms_code")  # 获取redis连接
            sms_code = redis_connection.get("%s_check" % username)
            # print(sms_code.decode())
            if sms_code is None:
                return None
            if password != sms_code.decode():
                return None
            return user
