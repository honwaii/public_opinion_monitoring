#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/5/3 0003 20:02
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : test_model.py

import fasttext
import jieba
import pandas as pd
from gensim.models import KeyedVectors


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


def split_data_set():
    rankings_col_name = ['label', 'comment']
    data = pd.read_csv("../datas/fast_text_dataset.txt", header=None, encoding='utf-8', names=rankings_col_name)
    shuffle_data = data.sample(frac=1.0).reset_index()
    train_num = int(shuffle_data.shape[0] * 0.8)
    train_data = shuffle_data.loc[0:train_num].drop(labels='index', axis=1)
    test_data = shuffle_data.loc[train_num + 1:].drop(labels='index', axis=1)
    train_data.to_csv("../datas/train_data.csv", index=False, header=False)
    test_data.to_csv("../datas/test_data.csv", index=False, header=False)
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


def train():
    # vec = KeyedVectors.load_word2vec_format('./pretrained/sgns.wiki.model')
    classifier = fasttext.train_supervised(input='../datas/train_data.csv', epoch=10, lr=0.005, label='__lable__',
                                           dim=150)
    print_results(*classifier.test('../datas/test_data.csv'))
    classifier.save_model('./sentiment_analysis_model_0.005_150_10')
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
with open('./datas/中文停用词表.txt', encoding='utf-8') as reader:
    stop_words = reader.read().split("\n")
#
classifier = fasttext.load_model('./model/sentiment_analysis_model')
