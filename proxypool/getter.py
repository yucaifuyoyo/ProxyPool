from .utils import get_page
from pyquery import PyQuery as pq
import re


class ProxyMetaclass(type):
    """
        元类，在FreeProxyGetter类中加入
        __CrawlFunc__和__CrawlFuncCount__
        两个参数，分别表示爬虫函数，和爬虫函数的数量。
    """

    def __new__(cls, name, bases, attrs):
        count = 0
        attrs['__CrawlFunc__'] = []
        for k, v in attrs.items():
            if 'crawl_' in k:
                attrs['__CrawlFunc__'].append(k)
                count += 1
        attrs['__CrawlFuncCount__'] = count
        return type.__new__(cls, name, bases, attrs)


class FreeProxyGetter(object, metaclass=ProxyMetaclass):
    def get_raw_proxies(self, callback):
        proxies = []
        print('Callback', callback)
        for proxy in eval("self.{}()".format(callback)):
            print('Getting', proxy, 'from', callback)
            proxies.append(proxy)
        return proxies

    def crawl_kuaidaili(self):
        for page in range(1, 10):
            # 快代理
            start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile(
                '<td data-title="IP">(.*)</td>\s*<td data-title="PORT">(\w+)</td>'
            )
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_xicidaili(self):
        # 西刺免费代理IP
        for page in range(1, 5):
            start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
            html = get_page(start_url)
            ip_adress = re.compile(
                '<td class="country"><img src="//fs.xicidaili.com/images/flag/cn.png" alt="Cn" /></td>\s*<td>(.*?)</td>\s*<td>(.*?)</td>'
            )
            # \s* 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_daili66(self, page_count=10):
        # 66免费代理网
        start_url = 'http://www.66ip.cn/{}.html'
        urls = [start_url.format(page) for page in range(1, page_count + 1)]
        for url in urls:
            print('Crawling', url)
            html = get_page(url)
            if html:
                doc = pq(html)
                trs = doc('.containerbox table tr:gt(0)').items()
                for tr in trs:
                    ip = tr.find('td:nth-child(1)').text()
                    port = tr.find('td:nth-child(2)').text()
                    yield ':'.join([ip, port])

    def crawl_data5u(self):
        # 无忧代理
        start_url = 'http://www.data5u.com/'
        html = get_page(start_url)
        ip_adress = re.compile(
            '<ul class="l2">\s*<span><li>(.*?)</li></span>\s*<span style="width: 100px;"><li class=".*">(.*?)</li></span>'
        )
        # \s * 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(str(html))
        for adress, port in re_ip_adress:
            result = adress + ':' + port
            yield result.replace(' ', '')

    def crawl_31f(self):
        # 三一代理
        start_url = 'http://31f.cn/'
        html = get_page(start_url)
        ip_adress = re.compile(
            '<td>([\d\.]+?)</td>\s*<td>(\d+)</td>'
        )
        # \s * 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(str(html))
        for adress, port in re_ip_adress:
            result = adress + ':' + port
            yield result.replace(' ', '')

    def crawl_ihuan(self):
        # 小幻代理
        start_url = 'https://ip.ihuan.me/'
        html = get_page(start_url)
        ip_adress = re.compile('>([\d\.]+?)</a></td><td>(\d+)</td>')
        # \s * 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(str(html))
        for adress, port in re_ip_adress:
            result = adress + ':' + port
            yield result.replace(' ', '')

    def crawl_superfastip(self):
        # 极速数据
        for i in range(1, 10):
            start_url = 'http://www.superfastip.com/welcome/freeip/{}'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile('>([\d\.]+?)</a></td><td>(\d+)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_89ip(self):
        # 89免费代理
        for i in range(1, 10):
            start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
            html = get_page(start_url)
            ip_adress = re.compile('''<td>
            ([\d\.]+?)      </td>
        <td>
            (\d+)       </td>''')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')

    def crawl_xiladaili(self):
        # 西拉免费代理
        start_url = 'http://www.xiladaili.com/'
        html = get_page(start_url)
        ip_adress = re.compile('<td>([\d\.]+?):(\d+)</td>')
        # \s * 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(str(html))
        for adress, port in re_ip_adress:
            result = adress + ':' + port
            yield result.replace(' ', '')

    def crawl_iphai(self):
        # ip海免费代理
        start_url = 'http://www.iphai.com/'
        html = get_page(start_url)
        ip_adress = re.compile('''<td>
                            ([\d\.]+?)                        </td>
                                            <td>
                            (\d+)                        </td>''')
        # \s * 匹配空格，起到换行作用
        re_ip_adress = ip_adress.findall(str(html))
        for adress, port in re_ip_adress:
            result = adress + ':' + port
            yield result.replace(' ', '')
