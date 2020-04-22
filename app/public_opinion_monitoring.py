#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 0014 20:56
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : public_opinion_monitoring.py
import os
import sys

sys.path.append(sys.path[0])
from app.util.cfg_operator import configuration as config
from flask import Flask, render_template, request, url_for, redirect
import app.service.data_handler as dh

app = Flask(__name__)


@app.route("/")
def index():
    return render_template("index.html")


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
# if __name__ == "__main__":
#     app.run(debug=True)
#     dh.schedule_task()
