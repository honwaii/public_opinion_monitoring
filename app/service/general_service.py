#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 0024 0:30
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : general_service.py
import datetime
import time
from collections import defaultdict
from functools import reduce

import jieba

from app.service import db_operation

from matplotlib import pyplot as plt


def check_user_permission(user, password):
    if user is None or password is None:
        return False
    sql = 'select * from pom_user where user_name="' + user + '"'
    user_info = db_operation.query_data(sql)
    if len(user_info) == 0 or password != user_info[0]['password']:
        return False
    return True


def register_account(user, password, cellphone):
    find_user_sql = 'select * from pom_user where user_name="' + user + '" or phone_number=' + cellphone
    print(find_user_sql)
    existed_user = db_operation.query_data(find_user_sql)
    if len(existed_user) != 0:
        return 0, '用户名或手机已注册.'
    sql = 'insert into pom_user (user_name,password,phone_number) values (%s,%s,%s)'
    db_operation.insert_with_param(sql, (user, password, cellphone))
    return 1, '您已成功注册.'


def find_password(user, password, cellphone):
    find_sql = 'select * from pom_user where user_name="' + user + '" or phone_number=' + cellphone
    existed_user = db_operation.query_data(find_sql)
    if len(existed_user) == 0:
        return 0, '该用户未注册.'
    sql = 'update pom_user set user_name="' + user + '",password="' + password + '",phone_number=' + cellphone + \
          ' where user_name="' + user + '" or phone_number=' + cellphone
    print(sql)
    db_operation.insert_or_update_data(sql)
    return 1, '密码修改成功.'


def get_shops_id():
    sql = 'SELECT DISTINCT shop_id from pom_shop_comment'
    result = db_operation.query_data(sql)
    shop_id_list = []
    if len(result) != 0:
        shop_id_list = [x['shop_id'] for x in result]
    return shop_id_list


def get_latest_timestamp():
    query_shops_sql = 'SELECT DISTINCT shop_id from pom_shop_comment'
    shops = db_operation.query_data(query_shops_sql)
    shop_latest_comment = defaultdict()
    for shop in shops:
        sql = 'select timestamp from pom_shop_comment where shop_id=' + str(
            shop['shop_id']) + ' order by `timestamp` desc limit 1 '
        d = db_operation.query_data(sql)
        shop_latest_comment[shop['shop_id']] = d[0]['timestamp'].timestamp()
    return shop_latest_comment


def score_statistics():
    sql = 'select score,count(*) count FROM pom_shop_comment GROUP BY score'
    result = db_operation.query_data(sql)
    score_count = {}
    for each in result:
        score_count[each['score']] = each['count']
    return score_count


def get_key_words_by_score():
    score_key_words = {}
    for score in range(1, 6):
        sql = 'SELECT score,key_word,COUNT(key_word) count from pom_shop_comment where score=' + str(
            score) + ' GROUP BY key_word ORDER BY count desc LIMIT 10'
        result = db_operation.query_data(sql)
        key_words = []
        for each in result:
            if len(str(each['key_word']).strip()) == 0:
                continue
            key_words.append(each['key_word'])
        key_words_str = reduce(lambda x, y: x + '、' + y, key_words)
        score_key_words[score] = key_words_str
    return score_key_words


def plot_statistic_image():
    scores = score_statistics()
    plt.rcParams['font.sans-serif'] = ['SimHei']
    plt.figure(figsize=(9, 7))
    labels = [u'情感得分:1', u'情感得分:2', u'情感得分:3', u'情感得分:4', u'情感得分:5']
    sizes = [x['count'] for x in scores]
    plt.pie(sizes, labels=labels, labeldistance=1.05, autopct='%3.1f%%', shadow=False, startangle=45, pctdistance=0.8)
    plt.title("平台商铺评论评分统计")
    plt.axis('equal')
    plt.legend()
    plt.savefig('../static/scores.png')
    plt.show()


def top_rating_shop(top_n):
    sql = 'SELECT shop_id,avg(score) avg_score,shop_name\
            FROM pom_shop_comment a,pom_shop b\
            WHERE a.shop_id=b.poi_id\
            GROUP BY shop_id ORDER BY avg_score DESC limit ' + str(top_n)
    result = db_operation.query_data(sql)
    return result


def plot_top_rated_shop():
    top_shops = top_rating_shop(10)
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体 SimHei为黑体
    plt.figure(figsize=(12, 4.8))
    x = []
    for shop in top_shops:
        t = jieba.lcut(shop['shop_name'])
        if len(t) > 5:
            t.insert(5, '\n')
        if len(t) > 10:
            t.insert(10, '\n')
        name = reduce(lambda x, y: x + y, t)
        x.append(name)
    x.reverse()
    y = [x['avg_score'] for x in top_shops]
    y.reverse()
    plt.rcParams['savefig.dpi'] = 300
    plt.title('评分排名前十的店铺')
    plt.xlabel('平均得分')
    plt.ylabel('店铺名称')
    plt.barh(x, y, )
    plt.savefig('../static/top_n.png', dpi=300)
    plt.show()


def get_all_comments():
    sql = 'select id,comment from pom_shop_comment'
    result = db_operation.query_data(sql)
    return result


def save_key_word(id, key_word):
    sql = 'update pom_shop_comment set key_word="' + key_word + '" where id="' + str(id) + '"'
    db_operation.insert_or_update_data(sql)
    return


def get_shop_key_words(shop_id):
    sql = 'SELECT key_word,COUNT(key_word) count from pom_shop_comment where shop_id=' + str(shop_id) + \
          ' GROUP BY key_word ORDER BY count desc limit 10'
    print(sql)
    result = db_operation.query_data(sql)
    filtered_result = []
    key_words = []
    for each in result:
        if len(str(each['key_word']).strip()) == 0:
            continue
        filtered_result.append(each)
        key_words.append(each['key_word'])
    return filtered_result, key_words


def get_shop_good_rating(shop_id):
    sql = 'select count(*) count FROM pom_shop_comment where shop_id="' + str(
        shop_id) + '" and (score =5 or score= 4 or score =3)'
    total_sql = 'select count(*) count from pom_shop_comment where shop_id="' + str(shop_id) + '"'
    good_count = db_operation.query_data(sql)[0]['count']
    total_count = db_operation.query_data(total_sql)[0]['count']
    good_rating = str(round(float(good_count) / float(total_count) * 100, 2)) + '%'
    return good_rating


t = get_shop_good_rating(1696868)
print(t)
# plot_top_rated_shop()
# plot_statistic_image()
