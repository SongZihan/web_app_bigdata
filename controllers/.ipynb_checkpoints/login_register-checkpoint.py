# -*- coding: utf-8 -*-
from flask import Blueprint, render_template, request, session, url_for, jsonify
from flask_login import login_user
from werkzeug.security import generate_password_hash, check_password_hash

from application import db
from common.models.user import User
from common.libs.Helper import ops_renderJSON, ops_renderErrJSON
from common.libs.DataHelper import getCurrentTime, Register, Login

login_page = Blueprint("login_page", __name__)


@login_page.route("/", methods=["GET", "POST"])
def login():
    """
    login 模板函数用来管理用户登录以及发放cookie
    """
    if request.method == "GET":
        return render_template("login_page.html")
    form = Login(request.form)
    if form.validate():
        user = User.query.filter_by(login_name=form.username.data).first()
        # 使用check_password_hash验证用户密码，其中第一个参数是数据库中查询的用户加密密码，第二个参数是用户输入的密码
        if user and check_password_hash(user._login_pwd, form.password.data):
            # 通过验证的话就使用flask-login想客户端发送cookie
            login_user(user)
            return ops_renderJSON(msg="login success~~")
        else:
            return ops_renderErrJSON(msg="密码错误")
    else:
        return ops_renderErrJSON(msg=str(form.errors))


@login_page.route("/registered", methods=["GET", "POST"])
def registered():
    if request.method == "GET":
        return render_template("Registered_page.html")
    form = Register(request.form)
    if form.validate():
        # 将用户信息注册进数据库
        model_user = User()
        model_user.login_name = form.username.data
        # 使用加密方法存储密码
        model_user._login_pwd = generate_password_hash(form.password.data)
        model_user.created_time = model_user.updated_time = getCurrentTime()
        try:
            db.session.add(model_user)
            db.session.commit()
        except Exception as error:
            return ops_renderErrJSON(msg=str(error))
        else:
            return ops_renderJSON(msg="注册成功~~")
    else:
        # 返回表单验证中的错误信息
        return ops_renderJSON(msg=str(form.errors))
