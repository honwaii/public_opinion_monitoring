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
from app.service import general_service


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


def get_shop_comment():
    shop_info = pd.read_csv('../datas/bsnInfo.csv', encoding='utf-8', usecols=['poiId'])
    shop_id_list = []
    for item in shop_info.itertuples():
        shop_id_list.append(item[1])
    shop_id_list = general_service.get_shops_id()
    proxy_ip_list = get_proxy_ip()
    for shop_id in shop_id_list:
        if str(shop_id) in shop_id_list:
            continue
        # url = 'http://www.meituan.com/meishi/' + str(shop_id) + '/'
        url_start = 'https://hz.meituan.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }
        proxies = random.choice(proxy_ip_list)
        print(proxies)
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
            time.sleep(random.randint(5, 60))
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
    proxy_ip_list = get_proxy_ip()
    for shop_id in shop_id_list:
        url_start = 'https://hz.meituan.com/'
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
        }
        proxies = random.choice(proxy_ip_list)
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


def get_proxy_ip():
    url = 'http://www.xicidaili.com/nn/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.129 Safari/537.36'
    }
    page = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(page.text, 'lxml')
    taglist = soup.find_all('tr', attrs={'class': re.compile("(odd)|()")})
    ip_list = []
    for trtag in taglist:
        tdlist = trtag.find_all('td')
        proxy = {'http': 'http://' + tdlist[1].string + ':' + tdlist[2].string}
        ip_list.append(proxy)
    # print(ip_list)
    return ip_list


get_shop_comment()
# if __name__ == '__main__':
#     # url = 'http://www.xicidaili.com/nn/'
#     url = 'https://www.xicidaili.com/nn/'
#     ip_list = get_ip_list(url)
#     proxies = get_random_ip(ip_list)
#     print(proxies)
