# -*- coding: utf-8 -*-
from flask import Blueprint,render_template,request,session,redirect,url_for,send_from_directory
from flask_login import login_required, current_user, logout_user

from application import db,app
from common.libs.HDFS_Manager import MyHDFS
from common.models.user import User
from common.libs.Helper import ops_renderJSON,ops_renderErrJSON,check_login,timeStamp
from common.libs.DataHelper import getCurrentTime
from hdfs import InsecureClient
import os

user_page = Blueprint( "user_page",__name__ )

@user_page.route("/dashboard",methods = ["GET","POST"])
@login_required
def dashboard():
    if request.method == "GET":
        cli = MyHDFS(current_user)
        if not cli.is_connection:
            return ops_renderErrJSON(msg="HDFS 连接失败!")
        context = {}
        context["username"] = cli.login_name
        return render_template("user_ui.html",**context)
    req = request.values
    if req["log_out"]:
        logout_user()
        return redirect(url_for("index_page.index"))


@user_page.route("/hdfs_res",methods = ["POST"])
@login_required
def hdfs_res():
    """
    用于获取hdfs上相关目录信息，以及对目录各层查看提供响应
    """
    if request.method == "POST":
        req = request.values
        content = {}
        cli = MyHDFS(current_user)
        if not cli.is_connection:
            return ops_renderErrJSON(msg="HDFS 连接失败!")
        # 获取首页的目录
        if "first_get" in req:
            content = cli.make_complete_path("/lake/")
            return ops_renderJSON(data=content)
        # 进入点击的下一级
        if "path" in req:
            content = cli.make_complete_path("/lake/" + req["path"])
            return ops_renderJSON(data=content)
        # 返回上一级
        if "path_back" in req:
            content = cli.make_complete_path("/lake" + req["path_back"])
            return ops_renderJSON(data=content)


@user_page.route("/hdfs_upload_file",methods = ["POST"])
@login_required
def hdfs_upload_file():
    """
    用于接收用户上传文件的请求
    """
    cli = MyHDFS(current_user)
    if not cli.is_connection:
        return ops_renderErrJSON(msg="HDFS 连接失败!")
    result = cli.upload_file(request)

    return ops_renderJSON(msg="upload success!",data=result[1]) if result[0] == "upload success!" else ops_renderJSON(msg=result)


@user_page.route("/hdfs_manage_file",methods = ["POST"])
@login_required
def hdfs_manage_file():
    """
    处理新建文件夹，删除私有文件的请求
    """
    cli = MyHDFS(current_user)
    if not cli.is_connection:
        return ops_renderErrJSON(msg="HDFS 连接失败!")
    result = cli.delete_file_and_mkdir(request)
    return ops_renderJSON(msg=result[0], data=result[1])


    # req = request.values
    # client = InsecureClient("http://master:50070", session["uid"])
    # if req["action"] == "delete":
    #     # 匹配文件名，不允许用户删除不是自己所有的文件
    #     if req["path"][:7] == "/public":
    #         file_owner = client.status("/lake" + req["path"],True)["owner"]
    #         if file_owner != session["uid"]:
    #             return ops_renderJSON(msg="You can't delete other people's file or directory in public lake")
    #         else:
    #             client.delete("/lake" + req["path"])
    #             # 传回修改后刷新的路径
    #             content = make_complete_path("/lake" + req["previous_path"])
    #             return ops_renderJSON(msg="success deleted",data = content)
    #     elif req["path"][:4]=="/usr" and req["path"][5:5+len(session["uid"])] != session["uid"]:
    #         return ops_renderErrJSON(msg="You can't delete file or directory in other's lake")
    #     else:
    #         client.delete("/lake" + req["path"])
    #         # 传回修改后刷新的路径
    #         content = make_complete_path("/lake" + req["previous_path"])
    #         return ops_renderJSON(msg="success deleted",data = content)
    # elif req["action"] == "mkdir":
    #     if req["path"][5:5+len(session["uid"])] == session["uid"]:
    #         try:
    #             client.makedirs("/lake" + req["path"])
    #         except:
    #             return ops_renderJSON(msg="make directory failed")
    #         else:
    #             # 传回修改后刷新的路径
    #             content = make_complete_path("/lake" + req["previous_path"])
    #             return ops_renderJSON(msg="make directory successed",data = content)
    #     elif req["path"][:7] == "/public":
    #         try:
    #             client.makedirs("/lake" + req["path"])
    #         except:
    #             return ops_renderJSON(msg="make directory failed")
    #         else:
    #             # 传回修改后刷新的路径
    #             content = make_complete_path("/lake" + req["path"])
    #             return ops_renderJSON(msg="make directory successed",data = content)
    #     else:
    #         return ops_renderJSON(msg="You can't make directory in other's lake")


@user_page.route("/download/<path:file_path>",methods = ["GET"])
@login_required
def hdfs_download_file(file_path):
    """
    处理下载文件的请求
    """
    cli = MyHDFS(current_user)
    if not cli.is_connection:
        return ops_renderErrJSON(msg="HDFS 连接失败!")
    client = cli.this_connection

    if file_path[4:5+len(MyHDFS.login_name)] == MyHDFS.login_name or file_path[:6] == "public":
        try:
            client.download("/lake/" + file_path,"download_cache/",True)
        except Exception as error:
            return ops_renderErrJSON(msg=str(error))
        file_name = file_path.split("/")[-1]
        # 为了解决文件缓存问题，可以考虑使用html和js在文件下载完成后返回一个响应请求
        return send_from_directory("download_cache/",file_name,as_attachment=True)
    else:
        return ops_renderErrJSON(msg="You can't download other's file")
        

        




