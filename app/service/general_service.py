#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/24 0024 0:30
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : general_service.py
from app.service import db_operation


def check_user_permission(user, password):
    if user is None or password is None:
        return False
    sql = 'select * from pom_user where user_name="' + user + '"'
    user_info = db_operation.query_data(sql)[0]
    if user_info is None or password != user_info['password']:
        return False
    return True
