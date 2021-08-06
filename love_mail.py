# -*- encoding: utf-8 -*-
'''
@File    :   love_mail.py
@Time    :   2021/08/06 16:06:08
@Author  :   fuhei 
@Version :   1.0
@Blog    :   http://www.lovei.org
'''
import smtplib
from email.mime.text import MIMEText
import string
import datetime
import requests
import re
import bs4
from bs4 import BeautifulSoup
import time 
import random,sys

reload(sys)
sys.setdefaultencoding('utf8') 
# 下面这些配置根据自己实际情况配置
boy_name = '****'
girl_name = '****'  
province = 'zhejiang'   #省份,
city = 'hangzhou'   #城市
special_day = '2021-08-06'  #纪念日
mailto_list=["****"] #发给哪个邮箱
mail_host="smtp.exmail.qq.com"  #设置邮箱服务器
mail_user="****"    #用户名
mail_pass="****"   #密码
name = '****'   #邮件发件人名称
mail_title = '****' #邮件名称

def get_day():
    d1 = datetime.datetime.strptime(special_day, '%Y-%m-%d')
    d2 = datetime.datetime.strptime(datetime.datetime.now().strftime('%Y-%m-%d'), '%Y-%m-%d')
    delta = d2 - d1
    return delta.days

def get_weathertip():
    url = "https://tianqi.moji.com/weather/china/%s/%s"%(province,city)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"html5lib",from_encoding="utf-8")
    all_tertiaryconsumers = soup.find_all(class_='wea_tips clearfix')
    for tertiaryconsumer in all_tertiaryconsumers:
        return re.search('<em>(.+?)</em>',str(tertiaryconsumer)).group(1)

def get_chp():
    url = "https://chp.shadiao.app/api.php"
    resp = requests.get(url)
    return resp.text

def get_weather():
    url = "https://tianqi.moji.com/weather/china/%s/%s"%(province,city)
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text,"html5lib",from_encoding="utf-8")
    all_tertiaryconsumers = soup.find_all(class_='days clearfix') 
    html = ''
    for tertiaryconsumer in all_tertiaryconsumers:
        day = tertiaryconsumer.find(name='a').text
        url = re.search('src="(.+?)"',str(tertiaryconsumer)).group(1)
        weather = re.search('<img alt="(.+?)"',str(tertiaryconsumer)).group(1)
        temperature = re.search('(\w+° \/ \w+°)',str(tertiaryconsumer)).group(1)
        if 'level_1' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_1').text.strip()
            color = '#8fc31f'
        if 'level_2' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_2').text.strip()
            color = '#d7af0e'
        if 'level_3' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_3').text.strip()
            color = '#f39800'
        if 'level_4' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_4').text.strip()
            color = '#e2361a'
        if 'level_5' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_5').text.strip()
            color = '#5f52a0'
        if 'level_6' in str(tertiaryconsumer):
            WindLevel = tertiaryconsumer.find(class_='level_6').text.strip()
            color = '#631541'
        html += """<div style="display: flex;margin-top:5px;height: 30px;line-height: 30px;justify-content: space-around;align-items: center;">
        <span style="width:15%%; text-align:center;">%s</span>
        <div style="width:10%%; text-align:center;">
            <img style="height:26px;vertical-align:middle;" src='%s' alt="">
        </div>
        <span style="width:25%%; text-align:center;">%s</span>
        <div style="width:35%%; ">
            <span style="display:inline-block;padding:0 8px;line-height:25px;color:%s; border-radius:15px; text-align:center;">%s</span>
        </div>
        </div>
        """ % (day, url, temperature, color, WindLevel)
    return html

def get_image():
  url = "http://wufazhuce.com/"
  resp = requests.get(url)
  soup = BeautifulSoup(resp.text,"html5lib",from_encoding="utf-8")
  return re.search('src="(.+?)"',str(soup.find(class_='fp-one-imagen'))).group(1)

def get_today():
    i = datetime.datetime.now()
    date = "%s/%s/%s" % (i.year, i.month, i.day)
    return date

mail_content = """<!DOCTYPE html>
<html>

<head>
    <title>
    </title>
    <meta name="viewport" content="width=device-width,minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
    <link rel='stylesheet' href='/stylesheets/style.css' />
    
</head>

<body style="margin:0;padding:0;">
    <div style="width:100%; margin: 40px auto;font-size:20px; color:#5f5e5e;text-align:center">
        <span>今天是我们在一起的第</span>
        <span style="font-size:24px;color:rgb(221, 73, 73)"  >{0}</span>
        <span>天</span>
    </div>
    <div style="width:100%; margin: 0 auto;color:#5f5e5e;text-align:center">
        <span style="display:block;color:#676767;font-size:20px">{1}</span>
        <span style="display:block;color:#676767;font-size:20px">{2}</span>
        <span style="display:block;margin-top:15px;color:#676767;font-size:15px">近期天气预报</span>

{3}
    </div>
    <div style="text-align:center;margin:35px 0;">
            <span style="display:block;margin-top:55px;color:#676767;font-size:15px">{4} ❤️ {5}</span>
            <span style="display:block;margin-top:25px;font-size:22px; color:#9d9d9d; ">{6}</span>
             <img src='{7}' style="width:100%;margin-top:10px;"  alt="">
    </div>
    

</body>

</html>""".format(str(get_day()),get_weathertip(),get_chp(),get_weather(),boy_name,girl_name,get_today(),get_image())

def send_mail(to_list,sub,content):
    me=name+"<"+mail_user+">"
    msg = MIMEText(content,_subtype='html',_charset='utf-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ",".join(mailto_list)
    try:
        server = smtplib.SMTP_SSL(mail_host, 465)
        server.login(mail_user,mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception as e:
        print(str(e))
        return False
if __name__ == '__main__':
    if send_mail(mailto_list,mail_title,mail_content):
        print("发送成功")
    else:
        print("发送失败")

