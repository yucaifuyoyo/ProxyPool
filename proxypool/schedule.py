import time
from multiprocessing import Process
import asyncio
import aiohttp
from proxypool.db import RedisClient
from proxypool.error import ResourceDepletionError
from proxypool.getter import FreeProxyGetter
from proxypool.setting import *
from asyncio import TimeoutError


class ValidityTester(object):
    test_api = TEST_API

    def __init__(self):
        self._raw_proxies = None
        self._usable_proxies = []

    def set_raw_proxies(self, proxies):
        self._raw_proxies = proxies
        self._conn = RedisClient()

    async def test_single_proxy(self, proxy):
        """
        text one proxy, if valid, put them to usable_proxies.
        """
        try:
            async with aiohttp.ClientSession() as session:  # aiohttp 高效的异步检测
                try:
                    if isinstance(proxy, bytes):
                        proxy = proxy.decode('utf-8')
                    real_proxy = 'http://' + proxy
                    print('Testing', proxy)
                    async with session.get(self.test_api, proxy=real_proxy,
                                           timeout=get_proxy_timeout) as response:  # 检测代理
                        if response.status == 200:  # 判断相应状态码
                            self._conn.put(proxy)  # 可用代理入右侧数据库
                            print('Valid proxy', proxy)
                except Exception as e:  # 异常放弃代理
                    print('Invalid proxy', proxy)
        except Exception as e:
            print(e)
            pass

    def test(self):
        """
        aio test all proxies.
        """
        print('ValidityTester is working')


        try:
            loop = asyncio.get_event_loop()
            tasks = [self.test_single_proxy(proxy) for proxy in list(set(self._raw_proxies))]  # 循环检测每个代理是否可用
            # for i in range(int(int(len(tasks)) / 20) + 1):
            #     loop.run_until_complete(asyncio.wait(tasks[20 * i:20 * (int(i) + 1)]))
            loop.run_until_complete(asyncio.wait(tasks))
        # except ValueError:
        except Exception as e:
            print('Async Error: {}'.format(e))
            print('*' * 1000)
            # print('Async Error')


class PoolAdder(object):
    """
    add proxy to pool
    """

    def __init__(self, threshold):
        self._threshold = threshold
        self._conn = RedisClient()  # redis 连接
        self._tester = ValidityTester()  # 检测代理是否可用
        self._crawler = FreeProxyGetter()  # 各大网站抓取代理

    def is_over_threshold(self):
        """
        judge if count is overflow.
        """
        if self._conn.queue_len >= self._threshold:
            return True
        else:
            return False

    def add_to_queue(self):
        print('PoolAdder is working')
        proxy_count = 0
        while not self.is_over_threshold():
            for callback_label in range(self._crawler.__CrawlFuncCount__):  # 获取每个爬虫函数
                callback = self._crawler.__CrawlFunc__[callback_label]  # 执行每个函数
                raw_proxies = self._crawler.get_raw_proxies(callback)
                # test crawled proxies
                self._tester.set_raw_proxies(raw_proxies)
                self._tester.test()
                proxy_count += len(raw_proxies)
                if self.is_over_threshold():
                    print('IP is enough, waiting to be used')
                    break
            if proxy_count == 0:
                raise ResourceDepletionError


class Schedule(object):
    @staticmethod
    def valid_proxy(cycle=VALID_CHECK_CYCLE):  # VALID_CHECK_CYCLE 时间的参数 setting中配置
        """
        Get half of proxies which in redis
        定时检测器 检测redis数据库ip是否有效
        """
        conn = RedisClient()  # 连接redis数据库
        tester = ValidityTester()  # 检测代理是否可用的类
        while True:
            print('Refreshing ip')
            count = int(0.5 * conn.queue_len)  # 取出队列长度一般的代理
            if count == 0:
                print('Waiting for adding')
                time.sleep(cycle)
                continue
            raw_proxies = conn.get(count)
            tester.set_raw_proxies(raw_proxies)
            tester.test()
            time.sleep(cycle)

    @staticmethod
    def check_pool(lower_threshold=POOL_LOWER_THRESHOLD,  # 最小代理数量
                   upper_threshold=POOL_UPPER_THRESHOLD,  # 最大代理数量
                   cycle=POOL_LEN_CHECK_CYCLE):  # 间隔检测时间
        """
        If the number of proxies less than lower_threshold, add proxy
        """
        conn = RedisClient()
        adder = PoolAdder(upper_threshold)
        while True:
            if conn.queue_len < lower_threshold:
                adder.add_to_queue()
            time.sleep(cycle)

    def run(self):
        # run方法重新运行了两个进程
        print('Ip processing running')
        valid_process = Process(target=Schedule.valid_proxy)  # 定时检查redis数据库代理是否有效
        check_process = Process(target=Schedule.check_pool)  # 从网上获取代理进行筛选然后放到redis数据库中
        valid_process.start()  # 开启进程
        check_process.start()  # 开启进程
