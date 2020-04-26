#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 0014 20:56
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : public_opinion_monitoring.py
from flask import Flask, render_template, request
import app.service.data_handler as dh
from app.service import general_service

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("login.html")


@app.route("/pom/login", methods=["POST"])
def login():
    print(request.form)
    message = '用户名或密码错误.'
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
    message = "user error"
    return render_template('login.html', reg_message=message)


#
# @app.route("/public_opinion_monitoring")
# def public_opinion():
#     return render_template("public_opinion_monitoring.html")
#
#
# @app.route("/auto_abs_error/<message>")
# def error_auto_abs(message=None):
#     return render_template("public_opinion_monitoring.html", message=message)
#
#
# @app.route("/mostsim_words/")
# def most_similar_words():
#     return render_template("most_similar_words.html")
#
#
# @app.route("/error_mostsim_words/<message>")
# def error_most_similar_words(message=None):
#     return render_template("most_similar_words.html", message=message)
#
#
# @app.route("/history")
# def history():
#     return redirect(url_for('history_page', page=1))

dh.schedule_task()
if __name__ == "__main__":
    app.run(debug=True)
#     dh.schedule_task()
