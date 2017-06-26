import requests
from lxml import etree
from urllib import parse


class QiuBai(object):
    def __init__(self):
        self.haeders = {
            'User-Agent': ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) '
                           'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
        }
        self.queue = []
        self.session = requests.session()
        self.start_url = 'https://www.qiushibaike.com/text'
        self.num = 1
        self.user_id = {'s': 4994802}

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
        print('fetch url: ', url)
        resp = self.session.get(url)
        self.num += 1
        self.num = self.num if self.num < 36 else 1
        return resp.text

    def parse_resp(self, text):
        tree = etree.HTML(text)
        all_posts = tree.xpath('//div[starts-with(@class, "article block")]')
        for post in all_posts:
            if int(post.xpath('.//i[@class="number"]/text()')[0]) > 200 and not post.xpath('.//span[@class="contentForAll"]'):
                self.queue.append('\n'.join(post.xpath('.//div[@class="content"]//span/text()')))

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
        print(qiubai.queue.pop())
        qiubai.make_sure_20()
    print('输出停止。')
