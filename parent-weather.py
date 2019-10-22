from wxpy import *
import requests
from threading import Timer
from time import sleep


"""
本文原创：pk哥
公众号：Python知识圈（id：PythonCircle）
「Python知识圈」公众号定时分享大量有趣有料的 Python 爬虫和实战项目，值得你的关注。
关注后回复1024免费领取学习资料！
"""

bot = Bot(cache_path=True)  # 扫码登录微信，如果在Linux环境中运行，加一个参数 bot = Bot(console_qr=-2,cache_path=True)


def get_weather():
    url = 'http://v.juhe.cn/weather/index?cityname=上海&key=xxx'  # 城市名cityname和key值换成自己的
    weather_json = requests.get(url).json()
    temperature = weather_json['result']['today']['temperature']
    weather = weather_json['result']['today']['weather']
    week = weather_json['result']['today']['week']
    city = weather_json['result']['today']['city']
    dressing_advice = weather_json['result']['today']['dressing_advice']
    return temperature, weather, week, city, dressing_advice


while True:   # ！！！调试时记得先把while True注释掉，不然会一直重复发送失败，一天限制100次调用的，成功后再加上注释
    try:
        temperature, weather, week, city, dressing_advice = get_weather()
        # 发送到微信群里
        my_groups = bot.groups().search('你的群名称')[0]   # 换成发送信息的群名称
        msg = '今天是：' + week + '\n' \
              + city + '的天气：' + weather + '\n' \
              + '今天温度：' + temperature +'\n' \
              + '穿衣指南：' + dressing_advice
        print(msg)
        my_groups.send(msg)

        # 单独私发微信
        # my_friend = bot.friends().search(u'pk')[0]  # 此处是对方自己的昵称，不是微信号，也不是你的备注。
        # my_friend.send(msg)  # 发送文字

        t = Timer(86400, get_weather)  # Timer（定时器）是 Thread 的派生类，用于在指定时间后调用一个方法。
        t.start()
        t.join()
    # 异常处理，发送失败，发送提醒消息给自己
    except BaseException:
        my_friend = bot.friends().search(u'xxx')[
            0]  # 发送不成功，则发送消息给自己，提醒消息发送失败 xxx改成你自己微信的昵称
        my_friend.send(u'天气消息发送失败，请停止程序进行调试')
        sleep(600)


