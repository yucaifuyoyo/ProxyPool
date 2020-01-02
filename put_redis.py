import json
import time
import urllib.request

import redis

REDIS_HOST = "10.133.3.26"
REDIS_POST = 6379
REDIS_DATABASE = 6
REDIS_PASSWORD = ''


class redis_ip(object):

    def __init__(self):
        self.conn = redis.Redis(host=REDIS_HOST, port=REDIS_POST, password=REDIS_PASSWORD, db=REDIS_DATABASE)

        while True:
            self.get_proxy()
            time.sleep(5)

    def dele(self):
        # 删除redis数据
        self.conn.delete('proxies')

    def put(self, proxy):
        # 将数据插入右侧
        self.conn.rpush("proxies", proxy)

    def get_proxy(self):
        # 要访问的目标网页
        page_url = "http://dev.kdlapi.com/testproxy/"
        #  api接口，返回格式为json
        api_url = ""

        #  api接口返回的ip
        response = urllib.request.urlopen(api_url)
        json_dict = json.loads(response.read().decode('utf-8'))
        ip_list = json_dict['data']['proxy_list']
        for proxy in ip_list:
            self.dele()
            self.put(proxy)
