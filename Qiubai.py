import requests
from lxml import etree
from urllib import parse


class QiuBai(object):
    def __init__(self):
        self.queue = []
        self.session = requests.session()
        self.start_url = 'https://www.qiushibaike.com/text'
        self.num = 1
        self.user_id = {'s': 4993999}
        self.headers = {
            'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                           '(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        }

    @staticmethod
    def url_concat(url, args=None):
        if not args:
            return url
        if url[-1] not in ('?', '&'):
            url += '?' if '?' not in url else '&'
        return url + parse.urlencode(args)

    def get_next_url(self):
        url = self.start_url + '/page/' + str(self.num) + '/'
        return self.url_concat(url, args=self.user_id)

    def fetch_url(self, url):
        resp = self.session.get(url, headers=self.headers)
        self.num += 1
        return resp.text

    def parse_resp(self, text):
        tree = etree.HTML(text)
        all_posts = tree.xpath('//div[@class="content"]/span')
        self.queue.extend(all_posts)

    def start(self):
        url = self.start_url if self.num == 1 else self.get_next_url()
        resp_text = self.fetch_url(url)
        self.parse_resp(resp_text)

    def make_sure_20(self):
        while len(self.queue) < 20:
            qiubai.start()


if __name__ == '__main__':
    qiubai = QiuBai()
    qiubai.make_sure_20()
    print('已准备就绪，按任意键输出糗百，按q退出：')
    while True:
        word = input()
        if word.upper() == 'Q':
            break
        el = qiubai.queue.pop()
        print('\n'.join(el.xpath('.//text()')))
        qiubai.make_sure_20()
    print('输出停止。')
