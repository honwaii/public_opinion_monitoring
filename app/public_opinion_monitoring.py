#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time    : 2020/4/14 0014 20:56
# @Author  : honwaii
# @Email   : honwaii@126.com
# @File    : public_opinion_monitoring.py
import os

from app.util.cfg_operator import configuration

host = configuration.get_config('host')
print(host)
