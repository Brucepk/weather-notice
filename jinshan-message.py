from twilio.rest import Client
import requests
from threading import Timer
from time import sleep


"""
本文原创：pk哥
公众号：Python知识圈（id：PythonCircle）
「Python知识圈」公众号定时分享大量有趣有料的 Python 爬虫和实战项目，值得你的关注。
关注后回复1024免费领取学习资料！
"""


# def get_weather():
#     url = 'http://v.juhe.cn/weather/index?cityname=上海&key=b0da46b36d3a2cce53fac9cdf51dc98a'   # 城市名cityname和key值换成自己的
#     weather_json = requests.get(url).json()
#     temperature = weather_json['result']['today']['temperature']
#     weather = weather_json['result']['today']['weather']
#     week = weather_json['result']['today']['week']
#     city = weather_json['result']['today']['city']
#     dressing_advice = weather_json['result']['today']['dressing_advice']
#     return temperature, weather, week, city, dressing_advice

def get_msg():
    url = 'http://open.iciba.com/dsapi/'   # 金山词霸每日一句 api 链接
    html = requests.get(url)
    content = html.json()['content']  # 获取每日一句英文语句
    note = html.json()['note']        # 获取每日一句英文的翻译语句
    return content, note


while True:
    try:
        content, note = get_msg()
        msg_all = content + '\n' + note + '\n' + 'from 爱你的人'
        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = '输入你的account_sid'
        auth_token = '输入你的auth_token'
        client = Client(account_sid, auth_token)
        message = client.messages \
            .create(body=msg_all, from_='+输入你获得的免费号码', to='+输入你验证的接收号码')
        print(message.sid)
        print(msg_all)

        t = Timer(86400, get_msg)  # Timer（定时器）是 Thread 的派生类，用于在指定时间后调用一个方法。
        t.start()
        t.join()
    # 异常处理，发送失败
    except:
        print('发送失败')
        break
