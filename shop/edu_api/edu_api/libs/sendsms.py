import requests


class Message(object):
    def __init__(self, api_key):
        # 账号唯一标识
        self.api_key = api_key
        # 单条短信发送接口
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_message(self, phone, code):
        """
        短信发送的实现
        :param phone: 前端传递的手机号
        :param code: 随机验证码
        :return:
        """
        params = {
            "apikey": self.api_key,
            'mobile': phone,
            'text': "【焦诚test】您的验证码是{code}".format(code=code)
        }
        # 可以发送http请求
        req = requests.post(self.single_send_url, data=params)
        print(req)


if __name__ == '__main__':
    message = Message("a19280256a714bad71b4b6cceb13a980")
    message.send_message("13513541278", "1234")
