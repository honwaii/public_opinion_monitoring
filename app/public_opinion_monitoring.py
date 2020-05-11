#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 0014 20:56
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : public_opinion_monitoring.py
from functools import reduce

from flask import Flask, render_template, request

from app.service import general_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/home")
def home():
    return render_template("index.html")


@app.route("/pom/login", methods=["POST"])
def login():
    print(request.form)
    message = '用户名密码错误或未注册.'
    user = request.form.get("user")
    password = request.form.get("password")
    if len(user) <= 0 or len(password) <= 0:
        return render_template('login.html', message=message)
    result = general_service.check_user_permission(user, password)
    if result:
        # TODO 登录成功跳转的页面
        return render_template("index.html")
    return render_template('login.html', message=message)


@app.route("/pom/register", methods=["POST"])
def register():
    print(request.form)
    user = request.form.get('user')
    if user is None or len(str(user).strip()) == 0:
        message = '用户名不能为空.'
        return render_template('error.html', err_message=message)
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if password1 != password2:
        message = '两次输入的密码不一致.'
        return render_template('error.html', err_message=message)
    cellphone = request.form.get('cellphone')
    if len(str(cellphone).strip()) != 11:
        message = '输入的手机号不正确.'
        return render_template('error.html', err_message=message)
    result = general_service.register_account(user, password1, cellphone)
    if result == 0:
        message = result[1]
        return render_template('error.html', err_message=message)
    return render_template('login.html')


@app.route("/pom/reset", methods=["POST"])
def reset_password():
    user = request.form.get('user')
    if user is None or len(str(user).strip()) == 0:
        message = '用户名不能为空.'
        return render_template('error.html', err_message=message)
    password1 = request.form.get('password1')
    password2 = request.form.get('password2')
    if password1 != password2:
        message = '两次输入的密码不一致.'
        return render_template('error.html', err_message=message)
    cellphone = request.form.get('cellphone')
    if len(str(cellphone).strip()) != 11:
        print(cellphone)
        print(len(str(cellphone).strip()))
        message = '输入的手机号不正确.'
        return render_template('error.html', err_message=message)
    result = general_service.find_password(user, password1, cellphone)
    if result[0] == 0:
        return render_template('error.html', err_message=result[1])
    return render_template('login.html')


@app.route("/pom/comment/<shop_id>")
def get_shop_key_words(shop_id):
    return


@app.route("/get_statistic_detail")
def get_statistic_detail():
    score_count = general_service.score_statistics()
    core_key_words = general_service.get_key_words_by_score()
    results = []
    for score in range(1, 6):
        result = {'score': score, 'count': score_count[score], 'key_words': core_key_words[score]}
        results.append(result)
    return render_template('statistic_comment.html', results=results)


@app.route("/get_shop_rating_detail")
def get_shop_rating_detail():
    shop_ratings = general_service.top_rating_shop(10)
    count = 0
    results = []
    for each in shop_ratings:
        good_rating = general_service.get_shop_good_rating(each['shop_id'])
        _, key_words = general_service.get_shop_key_words(each['shop_id'])
        words = reduce(lambda x, y: x + '、' + y, key_words)
        result = {'id': count + 1, 'name': each['shop_name'], 'score': each['avg_score'], 'rating': good_rating,
                  'key_words': words, 'shop_id': each['shop_id']}
        results.append(result)
        count += 1
    return render_template('shop_rating.html', results=results)


@app.route("/show_shop_comments/<shop_id>")
def show_shop_comments(shop_id):
    comments = general_service.get_good_comments_by_shop(shop_id)
    count = 0
    results = []
    for each in comments:
        result = {'id': count + 1, 'comment': each['comment'], 'score': each['score'], 'key_word': each['key_word'],
                  'timestamp': each['timestamp']}
        results.append(result)
        count += 1
    return render_template('shop_comments.html', results=results)


# dh.schedule_task()
if __name__ == "__main__":
    app.run(debug=True)
#     dh.schedule_task()
