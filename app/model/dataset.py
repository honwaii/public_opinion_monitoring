import re

from torchtext import data
import jieba
import logging

jieba.setLogLevel(logging.INFO)

regex = re.compile(r'[^\u4e00-\u9fa5aA-Za-z0-9]')


def word_cut(text):
    text = regex.sub(' ', text)
    return [word for word in jieba.cut(text) if word.strip()]


def get_dataset(path, text_field, label_field):
    text_field.tokenize = word_cut
    train, dev = data.TabularDataset(path=path + "\\random.csv", format='csv', skip_header=True, fields=[
        ('index', None),
        ('unnamed', None),
        ('unnamed', None),
        ('userId', None),
        ('restId', None),
        ('rating', label_field),
        ('rating_env', None),
        ('rating_flavor', None),
        ('rating_service', None),
        ('timestamp', None),
        ('comment', text_field)
    ]).split()
    print('++++')
    return train, dev


import pandas as pd

path = '../datas/'


def test():
    pd_ratings = pd.read_csv(path + 'ratings.csv')

    print('用户 数目：%d' % pd_ratings.userId.unique().shape[0])
    print('评分/评论 数目（总计）：%d\n' % pd_ratings.shape[0])

    print('总体 评分 数目（[1,5]）：%d' % pd_ratings[(pd_ratings.rating >= 1) & (pd_ratings.rating <= 5)].shape[0])
    print('环境 评分 数数目目（[1,5]）：%d' % pd_ratings[(pd_ratings.rating_env >= 1) & (pd_ratings.rating_env <= 5)].shape[0])
    print('口味 评分 （[1,5]）：%d' % pd_ratings[(pd_ratings.rating_flavor >= 1) & (pd_ratings.rating_flavor <= 5)].shape[0])
    print(
        '服务 评分 数目（[1,5]）：%d' % pd_ratings[(pd_ratings.rating_service >= 1) & (pd_ratings.rating_service <= 5)].shape[0])
    print('评论 数目：%d' % pd_ratings[~pd_ratings.comment.isna()].shape[0])
    print(pd_ratings.sample(5))

    return


def handle_data():
    pd_ratings = pd.read_csv(path + 'ratings_filtered.csv')
    pd.set_option('display.max_columns',None)
    print(pd_ratings.head(3))
    #
    # print('用户 数目：%d' % pd_ratings.userId.unique().shape[0])
    #
    print('评分/评论 数目（总计）：%d\n' % pd_ratings.shape[0])
    # p = pd_ratings.dropna(axis=0, how='any')
    # print('评分/评论 数目（总计）：%d\n' % p.shape[0])
    p = pd_ratings.sample(10000)
    p.to_csv(path + 'random.csv')
    # p = p.sample(10000)
    # p.to_csv(path + 'test_1.csv')

    return
# handle_data()
