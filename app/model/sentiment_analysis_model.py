#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/3 0003 20:02
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : test_model.py

import fasttext
import jieba
import pandas as pd


def handle_data():
    df_comment = pd.read_csv("../datas/general_ratings.csv", encoding="utf-8", usecols=['rating', 'comment'])
    with open('../datas/中文停用词表.txt', encoding='utf-8') as reader:
        stop_words = reader.read().split("\n")
    df_comment = df_comment.dropna()
    docs = []
    for item in df_comment.itertuples():
        rating = item[1]
        comment = item[2]
        process_text(rating, comment, stop_words, docs)
    write_data(docs, '../datas/fast_text_dataset.txt')
    return


def process_text(rating, comment, stop_words, docs):
    words = jieba.lcut(comment)
    words = filter(lambda x: len(x) > 1, words)
    words = filter(lambda x: x not in stop_words, words)
    docs.append("__lable__" + str(rating) + " , " + " ".join(words))
    return docs


def write_data(docs, output):
    with open(output, 'w', encoding='utf-8') as writer:
        for doc in docs:
            writer.write(doc + "\n")
        writer.flush()
        writer.close()


def train(saveDataFile):
    # vec = KeyedVectors.load_word2vec_format('./pretrained/sgns.wiki.model')
    classifier = fasttext.train_supervised(input='../datas/fast_text_dataset.txt', label='__lable__', dim=200)
    print_results(*classifier.test(saveDataFile))
    classifier.save_model('./sentiment_analysis_model')
    return


def print_results(N, p, r):
    print("N\t" + str(N))
    print("P@{}\t{:.3f}".format(1, p))
    print("R@{}\t{:.3f}".format(1, r))


def process_comment(comment, stop_words):
    comment = comment.replace("\n", "")
    comment = comment.replace("\r", "")
    words = jieba.lcut(comment)
    words = filter(lambda x: len(x) > 1, words)
    words = list(filter(lambda x: x not in stop_words, words))
    text = ''
    for word in words:
        text += " " + word
    return text


def train_word_vector_model():
    df = pd.read_csv("../datas/general_ratings.csv", encoding="utf-8", usecols=['comment'])
    df = df.dropna()
    docs = []
    for item in df.itertuples():
        comment = item[1]
        # process_text(rating, comment, stop_words, docs)
    write_data(docs, '../datas/fast_text_dataset.txt')
    model = fasttext.FastText
    model = fasttext.train_unsupervised('data.txt', model='skipgram', dim=200)
    model.save_model("vector_model.bin")
    fasttext.train_supervised()
    return


def predict(comment):
    cut_comment = process_comment(comment, stop_words)
    result = classifier.predict(cut_comment)
    return result[0][0].replace('__lable__', '')


# handle_data()
# train('../datas/fast_text_dataset.txt')
with open('../datas/中文停用词表.txt', encoding='utf-8') as reader:
    stop_words = reader.read().split("\n")
classifier = fasttext.load_model('../model/sentiment_analysis_model')
t = '位置不错，来西湖边上玩儿的时候来吃的，那种味道仿佛吸盘似的，刺激我的舌头，让我口水直流的酸味，强烈的震撼了我的食道和胃壁，让我食欲不由自主的燃起，再加上那种鲜活的酸味，跟咸中带甜的融合在一起，那种味道简直是难以形容的奥妙，原本因为热而丧失的那些活力，全部又再度出现了..酸酸甜甜的，沾酱的辣味有点刺激而浓郁，这个比我所知的四川风味红油酱味道还要丰富奥妙..菠菜清新的甜味，能让辣酱的辣味相得益彰'
r = predict(t)
print(r)
