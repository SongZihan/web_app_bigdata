# -*- coding: utf-8 -*-
#公用配置
DEBUG = True
SQLALCHEMY_ECHO = False
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ENCODING = "utf8mb4"
SECRET_KEY = "songzihan"
# 不禁用csrf会报错
WTF_CSRF_ENABLED = False

# DOMAIN = {
#     "www":"http://localhost:5000"
# }
# 应该要指定生产环境的ip HOST
DOMAIN = {
    "www":"http://15.165.115.5:80"
}