# -*- coding: utf-8 -*-
from flask import Flask
from flask_login import LoginManager
from flask_script import Manager
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

"""
登录验证
"""
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login_page.login'
login_manager.login_message = '请先登录或注册'

"""定义环境(local|server_test|production)"""
enviroment = "production"
if enviroment == "local":
    app.config.from_pyfile("config/local_setting.py")
elif enviroment == "server_test":
    app.config.from_pyfile("config/server_test_setting.py")
elif enviroment == "production":
    app.config.from_pyfile("config/production_setting.py")
else:
    print("please input correct environment(local|server_test|production)!")

db = SQLAlchemy(app)
