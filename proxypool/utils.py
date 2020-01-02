import asyncio
import random
import re

import aiohttp
import requests
from requests.exceptions import ConnectionError

from fake_useragent import UserAgent


def get_page(url, options={}):
    try:
        ua = UserAgent()
    except UnicodeDecodeError:
        pass
    base_headers = {
        'User-Agent': random.choice(ua),
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers, **options)
    print('Getting', url)
    try:
        r = requests.get(url, headers=headers, verify=False)
        print('Getting result', url, r.status_code)
        if r.status_code == 200:
            return r.text
    except ConnectionError:
        print('Crawling Failed', url)
        return None


class Downloader(object):
    """
    一个异步下载器，可以对代理源异步抓取，但是容易被BAN。
    """

    def __init__(self, urls):
        self.urls = urls
        self._htmls = []

    async def download_single_page(self, url):
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                self._htmls.append(await resp.text())

    def download(self):
        loop = asyncio.get_event_loop()
        tasks = [self.download_single_page(url) for url in self.urls]
        loop.run_until_complete(asyncio.wait(tasks))

    @property
    def htmls(self):
        self.download()
        return self._htmls


if __name__ == "__main__":
    options = {'Cookie': 'acw_sc__v2=5e0d93f931eaa798e664420e0756ae26f18cd0be'}
    start_url = 'https://proxy.mimvp.com/freeopen.php?proxy=in_hp&sort=&page=1'
    html = get_page(start_url).replace(' ', '').replace('	', '')
    print(html)
    ip_adress = re.compile(r'<td>([\d\.]+?)</td>\s*<td>(\d+)</td>')
    # \s* 匹配空格，起到换行作用
    re_ip_adress = ip_adress.findall(str(html))
    print(re_ip_adress)
    for adress, port in re_ip_adress:
        result = adress + ':' + port
        print(result.replace(' ', ''))
    print('-' * 100)

