#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 0014 20:56
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : public_opinion_monitoring.py
from flask import Flask, render_template, request

from app.service import general_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("login.html")


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


@app.route("/pom/statistic", methods=["POST"])
def get_statistic_detail():
    # general_service
    return


# dh.schedule_task()
if __name__ == "__main__":
    app.run(debug=True)
#     dh.schedule_task()
