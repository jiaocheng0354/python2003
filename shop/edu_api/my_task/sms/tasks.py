from edu_api.libs.sendsms import Message
from edu_api.settings import constants

from edu_api.my_task import app


@app.task(name="send_sms")
def send_sms(mobile, code):
    print("这是发送短信的方法")
    message = Message(constants.API_KEY)
    status = message.send_message(mobile, code)

    if not status:
        print("用户发送短信失败，手机号为：%s" % mobile)

    return "hello"