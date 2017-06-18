
# coding=utf-8
# 用requests模拟登录知乎，User-Agent设置成手机模式，跳过需要指出倒立字的验证码，用输入captcha形式的验证码

import re
import os
import requests

try:
    import cookielib
except:
    import http.cookiejar as cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar(filename='cookies.txt')

try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookie未加载')

user_agent = ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
              'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36')
headers = {
    'HOST': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'User-Agent': user_agent
}


def get_xsrf():
    login_url = 'https://www.zhihu.com'
    response = session.get(login_url, headers=headers)
    search_re = re.search('name="_xsrf" value="(.*?)"', response.text)
    if search_re:
        return search_re.group(1)
    return ""


def get_captcha():
    import time
    str_time = str(int(time.time()) * 1000)
    captcha_url = 'https://www.zhihu.com/' + 'captcha.gif?r={}&type=login'.format(str_time)
    captcha_resp = session.get(captcha_url, headers=headers)
    with open('checkout_captcha.gif', 'wb') as f:
        f.write(captcha_resp.content)
    os.startfile('checkout_captcha.gif')
    captcha = input('验证码: ')
    return captcha


def get_login(account, password):
    _xsrf = get_xsrf()
    headers.update({'X-Xsrftoken': _xsrf, 'X-Requested-With': 'XMLHttpRequest'})
    login_url = ""
    post_data = {
        '_xsrf': get_xsrf(),
        'password': password,
        # 'remember_me': 'true'
    }

    if re.match('1\d{10}', account):
        print('手机登录')
        login_url = 'https://www.zhihu.com/login/phone_num'
        post_data.update({'phone_num': account})
    elif '@' in account:
        print('邮箱登录')
        login_url = 'https://www.zhihu.com/login/email'
        post_data.update({'email': account})

    post_data['captcha'] = get_captcha()
    response = session.post(login_url, data=post_data, headers=headers)
    print(response.json())
    session.cookies.save()
    print('ok')


def get_index():
    response = session.get('https://www.zhihu.com', headers=headers)
    if '与世界分享你的知识、经验和见解' not in response.text:
        print('登录成功')
        with open('index.html', 'wb') as f:
            f.write(response.text.encode('utf8'))
        return
    print('登录失败')


get_login('xxx@email.com', 'password')
get_index()
