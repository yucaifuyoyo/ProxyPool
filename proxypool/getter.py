import re

from .utils import get_page


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
        try:
            for page in range(1, 4):
                # 快代理
                start_url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)
                html = get_page(start_url)
                ip_adress = re.compile(r'<td data-title="IP">([\d\.]+?)</td>\s*<td data-title="PORT">(\d+)</td>')
                re_ip_adress = ip_adress.findall(str(html))
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')
        except Exception as e:
            print('快代理 错误是:{}'.format(e))

    def crawl_xicidaili(self):
        try:
            # 西刺免费代理IP
            for page in range(1, 4):
                start_url = 'http://www.xicidaili.com/wt/{}'.format(page)
                html = get_page(start_url)
                ip_adress = re.compile(r'<td\D*</td>\s*<td>([\d\.]+?)</td>\s*<td>(\d+)</td>')
                # \s* 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(str(html))
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')
        except Exception as e:
            print('西刺免费代理IP 错误是:{}'.format(e))

    def crawl_daili66(self):
        try:
            # 66免费代理网
            for page in range(1, 4):
                start_url = 'http://www.66ip.cn/{}.html'.format(page)
                html = get_page(start_url)
                ip_adress = re.compile(r'<td>([\d\.]+?)</td><td>(\d+)</td><td>')
                # \s* 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(str(html))
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')
        except Exception as e:
            print('66免费代理网 错误是:{}'.format(e))

    def crawl_data5u(self):
        try:
            # 无忧代理
            start_url = 'http://www.data5u.com/'
            html = get_page(start_url)
            ip_adress = re.compile(r'<ul .*?">\s*<span><li>([\d\.]+?)</li></span>\s*<.*">(\d+)</li></span>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('无忧代理 错误是:{}'.format(e))

    def crawl_31f(self):
        try:
            # 三一代理
            start_url = 'http://31f.cn/'
            html = get_page(start_url)
            ip_adress = re.compile(r'<td>([\d\.]+?)</td>\s*<td>(\d+)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('三一代理 错误是:{}'.format(e))

    def crawl_superfastip(self):
        try:
            # 极速数据
            for i in range(1, 4):
                start_url = 'http://www.superfastip.com/welcome/freeip/{}'.format(i)
                html = get_page(start_url)
                ip_adress = re.compile(r'</tr>\s*<tr\D*\s*<td>([\d\.]+?)</td>\s*<td>(\d+)</td>')
                # \s * 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(str(html))
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')
        except Exception as e:
            print('极速数据 错误是:{}'.format(e))

    def crawl_89ip(self):
        try:
            # 89免费代理
            for i in range(1, 4):
                start_url = 'http://www.89ip.cn/index_{}.html'.format(i)
                html = get_page(start_url).replace(' ', '').replace('	', '')
                ip_adress = re.compile(r'<td>\s*([\d\.]+?)</td>\s*<td>\s*(\d+)</td>')
                # \s * 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(str(html))
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')
        except Exception as e:
            print('89免费代理 错误是:{}'.format(e))

    def crawl_xiladaili(self):
        try:
            # 西拉免费代理
            start_url = 'http://www.xiladaili.com/'
            html = get_page(start_url)
            ip_adress = re.compile('<td>([\d\.]+?):(\d+)</td>')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('西拉免费代理 错误是:{}'.format(e))

    def crawl_iphai(self):
        try:
            # ip海免费代理
            start_url = 'http://www.iphai.com/'
            html = get_page(start_url)
            ip_adress = re.compile('''<td>\s*([\d\.]+?)\s*</td>\s*<td>\s*(\d+)\s*</td>''')
            # \s * 匹配空格，起到换行作用
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('ip海免费代理 错误是:{}'.format(e))

    def crawl_xsdaili(self):
        try:
            # 小舒代理
            html = get_page('http://www.xsdaili.com/')
            ip_adress = re.compile(r'/dayProxy/ip/(\d+?).html')
            re_ip_adress = ip_adress.findall(str(html))
            html = get_page('http://www.xsdaili.com/dayProxy/ip/{}.html'.format(re_ip_adress[0]))
            ip_adress = re.compile(r'([\d\.]+?):(\d+)')
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('小舒代理 错误是:{}'.format(e))

    def crawl_zdaye(self):
        try:
            # 站大爷
            options = {'Cookie': 'acw_sc__v2=5e0d93f931eaa798e664420e0756ae26f18cd0be'}
            html = get_page('https://www.zdaye.com/dayProxy.html', options)
            ip_adress = re.compile(r'/dayProxy/ip/(\d+?).html')
            re_ip_adress = ip_adress.findall(str(html))
            html = get_page('https://www.zdaye.com/dayProxy/ip/{}.html'.format(re_ip_adress[0], options))
            ip_adress = re.compile(r'([\d\.]+?):(\d+)')
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('站大爷 错误是:{}'.format(e))

    def crawl_ip3366(self):
        try:
            for page in range(1, 4):
                # 云代理
                html = get_page('http://www.ip3366.net/?stype=1&page={}'.format(page))
                ip_adress = re.compile('''<tr>\s* <td>([\d\.]+?)</td>\s* <td>(\d+)</td>''')
                # \s* 匹配空格，起到换行作用
                re_ip_adress = ip_adress.findall(str(html))
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')
        except Exception as e:
            print('云代理 错误是:{}'.format(e))

    def crawl_freeip(self):
        try:
            for page in range(1, 4):
                # 高可用ip代理库
                start_url = 'https://www.freeip.top/?page={}'.format(page)
                html = get_page(start_url).replace(' ', '').replace('	', '')
                ip_adress = re.compile(r'<td>\s*([\d\.]+?)</td>\s*<td>\s*(\d+)</td>')
                re_ip_adress = ip_adress.findall(str(html))
                for adress, port in re_ip_adress:
                    result = adress + ':' + port
                    yield result.replace(' ', '')
        except Exception as e:
            print('高可用ip代理库 错误是:{}'.format(e))

    def crawl_nimadaili(self):
        try:
            # 尼玛id代理
            start_url = 'http://www.nimadaili.com/'
            html = get_page(start_url).replace(' ', '').replace('	', '')
            ip_adress = re.compile(r'<td>([\d\.]+?):(\d+)</td>')
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('尼玛id代理 错误是:{}'.format(e))

    def crawl_crossincode(self):
        try:
            # 免费代理ip
            start_url = 'https://lab.crossincode.com/proxy/ '
            html = get_page(start_url).replace(' ', '').replace('	', '')
            ip_adress = re.compile(r'<td>([\d\.]+?)</td>\s*<td>(\d+)</td>')
            re_ip_adress = ip_adress.findall(str(html))
            for adress, port in re_ip_adress:
                result = adress + ':' + port
                yield result.replace(' ', '')
        except Exception as e:
            print('免费代理ip 错误是:{}'.format(e))
