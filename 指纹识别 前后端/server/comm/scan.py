import random
import os
import requests
from bs4 import BeautifulSoup

# SSL配置
from app import models

verify_ssl = False
# 重定向配置
allow_redirects = True
# 忽略状态码配置
ignore_status_code = [400]

current_path = os.path.dirname(__file__)
user_agents = [i.strip() for i in open(os.path.join(current_path, 'useragents.txt'), "r").readlines()]

# 获取请求头信息
def getHeaders():

    headers = {
        'Accept': 'text/html,application/xhtml+xml,'
                  'application/xml;q=0.9,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': random.choice(user_agents),
    }

    return headers

# 获取 Cookie 信息
def getCookies():

    cookies = {}

    return cookies

# 获取超时范围
def getTimeOut():
    return 10

# 获取网页标题
def getTitle(html):

    soup = BeautifulSoup(html, 'lxml')

    if soup.title:
        return soup.title.text.strip()
    else:
        return "-- 未定义 --"

# 获取指定 app 信息
def getAppInfo(appId, resl):

    app = models.Apps.objects.filter(id=appId).first()
    if app.type == 0:
        checkArr('cms', resl, app)
    elif app.type == 1:
        checkArr('javascript', resl, app)
    elif app.type == 2:
        checkArr('server', resl, app)
    else:
        checkArr('other', resl, app)

# 指纹识别
def check(title, header, body):

    resl = {}

    titleFingers = models.Fingers.objects.filter(location=0).values()
    for tf in titleFingers:
        if tf['key'].strip().lower() in title.strip().lower():
            getAppInfo(tf['app_id'], resl)

    headeFingers = models.Fingers.objects.filter(location=1).values()
    for hf in headeFingers:
        if hf['key'].strip().lower() in header.strip().lower():
            getAppInfo(hf['app_id'], resl)

    bodyFingers = models.Fingers.objects.filter(location=2).values()
    for bf in bodyFingers:
        if bf['key'].strip().lower() in body.strip().lower():
            getAppInfo(bf['app_id'], resl)

    return resl

# 检查数组
def checkArr(key, resl, app):

    if key in resl.keys():
        isExit = False
        for item in resl[key]:
            if item['name'] == app.name:
                isExit = True
        if not isExit:
            resl[key].append({'name': app.name, 'detail': app.details})
    else:
        resl[key] = []
        resl[key].append({'name': app.name, 'detail': app.details})

def getWebInfo(url):

    '''
    响应内容：headers cont(标题)
    '''
    r = requests.get(url,
                     timeout=getTimeOut(),
                     headers=getHeaders(),
                     verify=verify_ssl,
                     cookies=getCookies(),
                     allow_redirects=allow_redirects)

    title = getTitle(r.content)

    if r.status_code==200:
        return {
            'title': title,
            'encoding': r.encoding,
            'status': r.status_code,
            'fingers': check(title, str(r.headers), str(r.content))
        }
    else:
        return {
            'title': title,
            'encoding': r.encoding,
            'status': r.status_code
        }

