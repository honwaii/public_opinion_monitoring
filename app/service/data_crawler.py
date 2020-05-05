#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/4 0004 19:48
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : data_crawler.py
import urllib.request
import csv
import random
from urllib import parse
import pandas as pd
import re
import json
import time

import requests
from bs4 import BeautifulSoup


def obtainData(page, csv_file, csv_writer):
    url = "https://hz.meituan.com/meishi/pn" + str(page) + "/"
    # Agent头
    Agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
    headers = {"User-Agent": Agent}
    req = urllib.request.Request(url, headers=headers)
    response = urllib.request.urlopen(req)
    html = str(response.read(), 'utf-8')
    pattern = re.compile(r'{"poiId":.*?}', re.S)
    item_list = pattern.findall(html)  # 获取数据
    print(item_list)
    for data in item_list:
        dictinfo = json.loads(data)
        print(dictinfo)
        csv_writer.writerow(
            [dictinfo["poiId"], dictinfo["title"], dictinfo["avgScore"], dictinfo["allCommentNum"], dictinfo["address"],
             dictinfo["avgPrice"]])


def get_shop_info():
    csv_file = open("../datas/bsnInfo.csv", "w", newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file, delimiter=',')
    csv_writer.writerow(['poiId', 'title', 'avgScore', 'allCommentNum', 'address', 'avgPrice'])
    for i in range(1, 11):
        time.sleep(3)
        print(f'第{i}页数据')
        obtainData(i)
    csv_file.close()


t = 'https://www.meituan.com/meishi/api/poi/getMerchantComment?' \
    'uuid=e43fc4d3-80bd-43cb-8aba-ee56aca5dacd' \
    '&platform=1' \
    '&partner=126&' \
    'originUrl=https%3A%2F%2Fwww.meituan.com%2Fmeishi%2F187008196%2F' \
    '&riskLevel=1' \
    '&optimusCode=10' \
    '&id=187008196' \
    '&userId=&offset=0&pageSize=10&sortType=1'


def get_shop_comment():
    shop_info = pd.read_csv('../datas/bsnInfo.csv', encoding='utf-8', usecols=['poiId'])
    shop_id_list = []
    for item in shop_info.itertuples():
        shop_id_list.append(item[1])
    ll = ["102059037",
          "158460006",
          "165049172",
          "1859117615",
          "187008196",
          "40981653",
          "4689539",
          "4804147",
          "4822571",
          "4895107",
          "5290811",
          "5661027",
          "6107631",
          "6233056",
          "6407438",
          "6530213",
          "4895107",
          "6587575",
          '773072892',
          '5103230',
          '1469192',
          '1927113121',
          '6054687',
          '6249139',
          '162811006',
          "1697705"
          ]
    for shop_id in shop_id_list:
        if str(shop_id) in ll:
            continue
        # url = 'http://www.meituan.com/meishi/' + str(shop_id) + '/'
        url_start = 'https://hz.meituan.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
            # 'User-Agent': random.choice(USER_AGENTS)

        }
        proxies = {"http": random.choice(PROXIES)}
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)
        cookie = s.cookies
        print(get_url(0, shop_id))
        response = s.get(url=get_url(0, shop_id), headers=headers, cookies=cookie, timeout=3, proxies=proxies)
        data = response.text
        if data is None:
            print("no data ")
            continue
        print(data)
        data = json.loads(data).get('data')
        total = int(data.get('total'))
        print('shop ' + str(shop_id) + '总共有：' + str(total))
        save_comment(shop_id, data)
        count = 1
        for offset in range(1, int(total / 50)):
            url = get_url(offset, shop_id)
            print(url)
            response = requests.get(url=url, headers=headers, proxies=proxies)
            data = response.text
            if data is None:
                print("no data ")
                continue
            data_dict = json.loads(data)
            save_comment(shop_id, data_dict.get('data'))
            if count == 10:
                count = 1
                break
            count += 1
            time.sleep(5 * count)
        print("shop_id " + str(shop_id) + ' have crawled.')
        time.sleep(30)
    return


def get_url(offset, shop_id):
    originUrl = parse.quote_plus('https://www.meituan.com/meishi/' + str(shop_id) + '/')
    url = 'https://www.meituan.com/meishi/api/poi/getMerchantComment?' \
          'uuid=e43fc4d3-80bd-43cb-8aba-ee56aca5dacd&platform=1&partner=126' \
          '&originUrl=' + originUrl + '&riskLevel=1&optimusCode=10&id=' + str(shop_id) + \
          '&userId=&offset={}&pageSize=100&sortType=1'.format(offset)
    return url


def save_comment(shop_id, data, path=None):
    for item in data.get('comments'):
        if path is None:
            path = r'../datas/mt_comment/{}.csv'.format(str(shop_id))
        with open(path, 'a', encoding='utf-8') as f:
            job_list = [item.get('comment'), item.get('star'), item.get('commentTime')]
            write = csv.writer(f)
            write.writerow(job_list)
    return


# 获取开源代理ip
def getListProxies():
    ip_list = []
    session = requests.session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'}
    page = session.get("http://www.xicidaili.com/nn", headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    for trtag in taglist:
        tdlist = trtag.find_all('td')
        proxy = {'http': 'http://' + tdlist[1].string + ':' + tdlist[2].string}
        ip_list.append(proxy)
    return ip_list


PROXIES = [
    "http://118.181.226.166:44640",
    "http://114.215.41.232:8080",
    "http://202.115.142.147:9200",
    "http://49.85.99.29:10098",
    "http://139.196.34.166:80",
    "http://120.79.139.253:8080",
    "http://124.112.104.84:4216",
    "http://27.188.62.3:8060",
    "http://121.17.210.114:8060",
    "http://223.215.101.143:4216",
    "http://223.215.100.90:4216",
    "http://60.188.11.110:3000",
    "http://223.215.103.243:4216",
    "http://117.69.152.162:8690",
    "http://115.199.131.42:8060",
    "http://183.166.249.36:4216",
    "http://125.123.153.85:3000",
    "http://121.36.210.88:8080",
    "http://124.193.110.231:8118",
    "http://106.122.205.90:8118",
    "http://58.215.219.2:8000",
    "http://211.149.252.155:8888",
    "http://117.45.139.230:9006",
    "http://139.224.16.103:8080",
    "http://121.233.87.33:4216",
    "http://122.235.188.241:8118",
    "http://117.69.153.238:4216",
    "http://183.166.253.96:4216",
    "http://118.187.58.34:53280",
    "http://125.123.157.194:3000",
    "http://49.85.84.225:10098",
    "http://125.123.154.160:3000",
    "http://114.228.205.11:8118",
    "http://114.104.142.191:8690",
    "http://123.168.67.96:8118",
    "http://114.226.163.169:8118",
    "http://125.123.156.148:3000",
    "http://125.123.152.159:3000",
    "http://183.166.139.23:9999",
    "https://117.114.149.66:53280",
    "http://115.206.100.87:8060",
    "http://117.88.177.127:3000",
    "http://211.142.169.4:808",
    "http://117.88.177.185:3000",
    "http://117.69.152.116:4216"
]

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50",
    "Opera/9.80 (Windows NT 6.1; U; zh-cn) Presto/2.9.168 Version/11.50",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    # "Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.48 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def get_random_ip(ip_list):
    proxy_list = []
    for ip in ip_list:
        proxy_list.append('http://' + ip)
    if len(proxy_list) == 0:
        print('no suitable proxy')
        return
    proxy_ip = random.choice(proxy_list)
    proxies = {'http': proxy_ip}
    return proxies


def get_real_comment():
    shop_info = pd.read_csv('../datas/bsnInfo.csv', encoding='utf-8', usecols=['poiId'])
    shop_id_list = []
    for item in shop_info.itertuples():
        shop_id_list.append(item[1])
    latest_data = {}
    for shop_id in shop_id_list:
        url_start = 'https://hz.meituan.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }
        proxies = {"http": random.choice(PROXIES)}
        s = requests.Session()
        s.get(url_start, headers=headers, timeout=3)
        cookie = s.cookies
        print(get_url(0, shop_id))
        response = s.get(url=get_url(0, shop_id), headers=headers, cookies=cookie, timeout=3, proxies=proxies)
        data = response.text
        if data is None:
            print("no data ")
            continue
        data = json.loads(data).get('data')
        latest_data[shop_id] = data
        save_comment(shop_id, data, path='./datas/latest_comment/{}.csv'.format(shop_id))

# get_shop_comment()
# if __name__ == '__main__':
#     # url = 'http://www.xicidaili.com/nn/'
#     url = 'https://www.xicidaili.com/nn/'
#     ip_list = get_ip_list(url)
#     proxies = get_random_ip(ip_list)
#     print(proxies)
