# coding: utf-8
from flask_login import UserMixin

from application import db, login_manager


class User(UserMixin,db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    login_name = db.Column(db.String(25), nullable=False, unique=True)
    _login_pwd = db.Column(db.String(150), nullable=False)
    status = db.Column(db.Integer, nullable=False, server_default="1")
    updated_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())
    created_time = db.Column(db.DateTime, nullable=False, server_default=db.FetchedValue())


# 获取用户login_name作为cookie加密
@login_manager.user_loader
def load_user(uid):
    return User.query.get(int(uid))
