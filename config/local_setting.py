# -*- coding: utf-8 -*-
# 本地开发环境配置文件
from config.base_setting import *
# SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql://root:songzihan@localhost/web_app"

SERVER_NAME = "localhost:5000"

SECRET_KEY = "songzihan"