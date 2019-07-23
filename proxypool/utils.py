import requests
import asyncio
import aiohttp
from requests.exceptions import ConnectionError
from fake_useragent import UserAgent, FakeUserAgentError
import random


def get_page(url, options={}):
    try:
        ua = UserAgent()
    except FakeUserAgentError:
        pass
    base_headers = {
        'User-Agent': ua.random,
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8'
    }
    headers = dict(base_headers, **options)
    print('Getting', url)
    try:
        r = requests.get(url, headers=headers)
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
    html = get_page('http://www.iphai.com/')
    print('*' * 100)
    print(html)
    print('*' * 100)
    import re
    # ip_adress = re.compile('<td>\s*([\d\.]+?)</td>\s*<td>\s*(\d+)</td>\s*<td>')
    ip_adress = re.compile('''<td>
                            ([\d\.]+?)                        </td>
                                            <td>
                            (\d+)                        </td>''')
    # \s* 匹配空格，起到换行作用
    re_ip_adress = ip_adress.findall(str(html))
    print(re_ip_adress)
    for adress, port in re_ip_adress:
        result = adress + ':' + port
        print(result.replace(' ', ''))
    print('-' * 100)


'''
<td>
			123.52.43.64		</td>
		<td>
			8118		</td>
'''

'''
<td class="country"><img src="//fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>
      <td>182.34.32.153</td>
      <td>9999</td>
'''


# https://www.baidu.com/s?wd=%E5%85%8D%E8%B4%B9%E4%BB%A3%E7%90%86%E7%BD%91%E7%AB%99&pn=20&oq=%E5%85%8D%E8%B4%B9%E4%BB%A3%E7%90%86%E7%BD%91%E7%AB%99&ie=utf-8&rsv_idx=1&rsv_pq=f499d8ae00070d8f&rsv_t=7f19HubaxP8B9AT0rP18mJAajqAymluZZ5lUtP1T1wjns1w6oD5OldGNIe8&rsv_page=1