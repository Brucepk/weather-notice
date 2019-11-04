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


def get_weather():
    url = 'http://v.juhe.cn/weather/index?cityname=上海&key=输入你自己的key，在v.juhe.cn网站注册获取'  # 城市名cityname和key值换成自己的
    weather_json = requests.get(url).json()
    temperature = weather_json['result']['today']['temperature']
    weather = weather_json['result']['today']['weather']
    week = weather_json['result']['today']['week']
    city = weather_json['result']['today']['city']
    dressing_advice = weather_json['result']['today']['dressing_advice']
    return temperature, weather, week, city, dressing_advice


while True:
    try:
        temperature, weather, week, city, dressing_advice = get_weather()

        msg = '今天是：' + week + '\n' \
              + city + '的天气：' + weather + '\n' \
              + '今天温度：' + temperature +'\n' \
              + '穿衣指南：' + dressing_advice
        print(msg)

        # Your Account Sid and Auth Token from twilio.com/console
        # DANGER! This is insecure. See http://twil.io/secure
        account_sid = '输入你的account_sid'
        auth_token = '输入你的auth_token'
        client = Client(account_sid, auth_token)

        message = client.messages \
            .create(body=msg, from_='输入你获取的号码', to='+输入你验证过的号码')
        print(message.sid)

        t = Timer(86400, get_weather)  # Timer（定时器）是 Thread 的派生类，用于在指定时间后调用一个方法。
        t.start()
        t.join()
    # 异常处理，发送失败
    except BaseException:
        print('发送失败')
        break