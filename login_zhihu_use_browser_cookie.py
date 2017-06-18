
# coding: utf-8
# 用chrome 的editthiscookie插件导出知乎cookies，组合成LWP-Cookies-2.0形式，即可直接用。

import requests

try:
    import cookielib
except:
    from http import cookiejar as cookielib

session = requests.session()
session.cookies = cookielib.LWPCookieJar('br_cookies.txt')

try:
    session.cookies.load(ignore_discard=True)
except:
    print('cookies未加载')


headers = {
    'HOST': 'www.zhihu.com',
    'Referer': 'https://www.zhihu.com',
    'User-Agent': ('Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) '
                   'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Mobile Safari/537.36')
}


def get_index():
    index_url = 'https://www.zhihu.com'
    resp = session.get(index_url, headers=headers)
    if '与世界分享你的知识、经验和见解' not in resp.text:
        print(resp.text)
        print('登录成功')
        return
    print('登录失败')


if __name__ == '__main__':
    get_index()
