import requests
import json
import time
import pymysql
import logging
import random
from lxml import etree

logging.basicConfig(
    level=logging.INFO,  # 定义输出到文件的log级别，大于此级别的都被输出
    format='%(asctime)s  %(filename)s  %(levelname)s : %(message)s',  # 定义输出log的格式
    datefmt='%Y-%m-%d %H:%M:%S',  # 时间
    filename='yibao.log',  # log文件名
    filemode='a')  # 写入模式“w”或“a”


class yibao(object):
    def __init__(self):
        self.db = pymysql.connect(host='localhost', port=3306, database='cfda', user='root', password='root',
                                  charset='utf8')
        self.cursor = self.db.cursor()
        self.headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36", }
        self.url = 'http://code.nhsa.gov.cn:8000/jbzd/public/toStdOperationTreeList.html'
        self.proxie = '47.98.163.18:8888'

        self.parse_page()

    def parse_page(self):
        while True:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
            proxiess = {'http': f'http://{self.proxie}', 'https': f'http://{self.proxie}'}
            try:
                html = requests.get('https://www.baidu.com/', headers=headers, verify=False, allow_redirects=False,
                                    proxies=proxiess, timeout=5).content.decode('utf-8')
                print('proxiess:', proxiess)
            except:
                self.proxie = requests.get('http://127.0.0.1:5000/get', headers=headers, verify=False).content.decode(
                    'utf-8')
                print('errar proxiess:', proxiess)
            print('*' * 100)
            time.sleep(5)


if __name__ == '__main__':
    yibao()
