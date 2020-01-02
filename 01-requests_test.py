import requests

# while True:
#     headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
#
#     ti = time.time()
#     proxies = requests.get('http://127.0.0.1:5000', headers=headers, verify=False).content.decode('utf-8')
#     print(proxies)
#     print(time.time()-ti)
#
#     ti = time.time()
#     proxies = requests.get('http://127.0.0.1:5000/get', headers=headers, verify=False).content.decode('utf-8')
#     print(proxies)
#     print(time.time()-ti)
#
#     time.sleep(5)

for i in range(100):
    proxies = requests.get('http://127.0.0.1:5000/get').content.decode('utf-8')
    print(proxies)

# payload = {'key1': 'value1', 'key2': 'value2'}
# proxies = {'http': 'http://47.98.163.18:8080', 'https': 'http://47.98.163.18:8080'}
# headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
# requests.get(url, headers=headers, verify = False, params=payload, allow_redirects=False, proxies=proxies).content.decode('utf-8')
