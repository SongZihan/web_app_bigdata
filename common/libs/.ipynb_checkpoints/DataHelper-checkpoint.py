# -*- coding: utf-8 -*-
import datetime
from flask_wtf import Form
from werkzeug.security import check_password_hash
from wtforms import TextField, StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired, Length, EqualTo
from common.models.user import User


def getCurrentTime(frm="%Y-%m-%d %H:%M:%S"):
    dt = datetime.datetime.now()
    return dt.strftime(frm)


class Login(Form):
    """
    用来提供登录表单验证的功能
    """
    username = StringField("username", validators=[DataRequired(message="请输入用户名"), Length(6, 25)])
    password = PasswordField("password", validators=[DataRequired(message="请输入密码"), Length(6, 25)])

    def validate_username(self, field):
        if not User.query.filter_by(login_name=field.data).first():
            raise ValidationError('没有找到用户名')


class Register(Form):
    """
    用来提供注册表单验证
    """
    username = StringField("username", validators=[DataRequired(message="请输入用户名"), Length(6, 25)])
    password = PasswordField("password", validators=[DataRequired(message="请输入密码"), Length(6, 25),
                                                     EqualTo('repeat_pwd', message='两次输入的密码不一致')])
    repeat_pwd = PasswordField("repeat_pwd", validators=[DataRequired()])

    def validate_username(self, field):
        if User.query.filter_by(login_name=field.data).first():
            raise ValidationError('用户名已被注册')
