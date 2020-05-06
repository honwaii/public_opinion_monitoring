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
