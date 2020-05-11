#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/5 0005 22:06
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : data_init_handle.py
import pandas as pd
from app.util.cfg_operator import config
from app.service import db_operation
import os
from app.model import sentiment_analysis_model as sam
import time
from app.service import general_service


def init():
    shop_info = pd.read_csv('bsnInfo.csv', encoding='utf-8', usecols=['poiId', 'title'])
    for item in shop_info.itertuples():
        sql = 'insert into pom_shop (poi_id,shop_name) values(%s,%s)'
        db_operation.insert_with_param(sql, (item[1], item[2]))


def handle_existed_comment(path=None):
    shop_info = pd.read_csv('../datas/bsnInfo.csv', encoding='utf-8', usecols=['poiId'])
    shop_id_list = []
    for item in shop_info.itertuples():
        shop_id_list.append(item[1])
    handled_shop = general_service.get_shops_id()
    rankings_col_name = ['comment', 'score', 'timestamp']
    for shop_id in shop_id_list:
        if path is None:
            path = '../datas/mt_comment/'
        file = path + str(shop_id) + '.csv'
        if not os.path.exists(file):
            print('file {} is not exist.'.format(file))
            continue
        if shop_id in handled_shop:
            print('data of shop ' + str(shop_id) + ' have handled.')
            continue
        comments = pd.read_csv(file, header=None, encoding='utf-8', names=rankings_col_name)
        comments = comments.dropna()
        for item in comments.itertuples():
            comment = item[1]
            score = sam.predict(comment)
            timestamp = float(item[3]) / 1000
            tmObject = time.localtime(timestamp)
            tmStr = time.strftime("%Y-%m-%d %H:%M:%S", tmObject)
            sql = 'insert into pom_shop_comment (shop_id,comment,score,timestamp) values(%s,%s,%s,%s)'
            db_operation.insert_with_param(sql, (shop_id, comment, score, tmStr))
    return


# handle_existed_comment()
