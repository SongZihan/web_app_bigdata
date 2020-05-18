# -*- coding: utf-8 -*-
#生产环境配置文件
from config.base_setting import *
DEBUG = False
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_DATABASE_URI = "mysql://root:songzihan@master/web_app"
