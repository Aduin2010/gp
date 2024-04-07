import threading

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.edge.options import Options
import requests
import json
import pytest

### 获取代理IP ###
def get_ip_list(i):

    i = int(i)
    url = 'http://d.jghttp.alicloudecs.com/getip?num=50&type=2&pro=0&city=0&yys=0&port=11&time=7&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=500000,510000,520000,530000'
    resp = requests.get(url)
    resp_json = resp.text
    resp_dict = json.loads(resp_json)
    ip_dict_list = resp_dict['data']
    ip_port = '{ip}:{port}'.format(ip=ip_dict_list[i].get('ip'), port=ip_dict_list[i].get('port'))
    # print(ip_port)
    return ip_port

### 爬-测试用 ###
def spider_ip(ip_port, url):
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
        'Connection': 'close'
    }
    proxies = {
        'https': 'http://{}'.format(ip_port)
    }

    try:
        resp = requests.get(url=url, headers=header, proxies=proxies, verify=False, timeout=7)
        result = resp.text
        # print('线程名称-', threading.current_thread(), '\n' + result)
        print(resp.status_code)

    except Exception as e:
        print(e)


def Fountion(i):

    print(i)
    a = get_ip_list(i)

    opt = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0'
    opt.add_argument('--headless')
    opt.add_argument('--disable-gpu')
    opt.add_argument(f'user-agent={user_agent}')
    opt.add_argument('--proxy-server=http://%s' % a)
    driver = webdriver.Edge(options=opt)
    # driver = webdriver.Edge()

    try:
        # https://www.zhipin.com/web/geek/job?query={job_type}&page={i}
        driver.get(f"https://myip.ipip.net")
        content = driver.page_source
        soup = BeautifulSoup(content, 'html.parser')
        print(threading.current_thread(), '\n')
        print(a)
        print(soup)

    except Exception as e:
        print(e)
###——————###

if __name__ == '__main__':
    for i in range(1, 4):
        ip_thread = threading.Thread(target=Fountion, args=(i,))
        ip_thread.name = '线程名称-->%d' % i
        ip_thread.start()
        ip_thread.join()
        #
        # Fountion(1)

