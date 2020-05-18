from hdfs import InsecureClient
import os
from common.libs.Helper import timeStamp


def make_complete_path(path):
    """
    输入完整的hdfs路径，输出组装好的html组件
    """
    content = {}
    c = InsecureClient("http://master:50070", session["uid"])
    content["path"] = []
    for k in c.list(path,True):
        if k[1]["type"] == "FILE":
            content["path"].append("<li class='is_file list_content list-group-item'><span class='file name'>"+k[0]+"</span><span class='badge'>"+k[1]["owner"]+"</span><span class='badge'>"+timeStamp(k[1]["modificationTime"])+"</span></li>")
        else:
            content["path"].append("<li class='is_list list_content list-group-item'><span class='list name'>"+k[0]+"</span><span class='badge'>"+k[1]["owner"]+"</span><span class='badge'>"+timeStamp(k[1]["modificationTime"])+"</span></li>")
    return content

class MyHDFS():
    """
    用来管理用户连接HDFS之后的一系列行为
    """
    is_connection = True
    this_connection = ""
    login_name = ""

    def __init__(self,current_user):
        # 需要将current_user对象传进来否则会报错
        self.login_name = current_user.login_name
        try:
            # 测试能否正常连接hdfs而已
            c = InsecureClient("http://master:50070", self.login_name)
            # 默认尝试给用户创建一个文件夹
            c.makedirs("/lake/usr/" + self.login_name)
        except Exception as error:
            self.is_connection = False
        else:
            self.this_connection = c

    def make_complete_path(self,path):
        """
            输入完整的hdfs路径，输出组装好的html组件
        """
        content = {}
        content["path"] = []
        for k in self.this_connection.list(path, True):
            if k[1]["type"] == "FILE":
                content["path"].append("<li class='is_file list_content list-group-item'><span class='file name'>" + k[
                    0] + "</span><span class='badge'>" + k[1]["owner"] + "</span><span class='badge'>" + timeStamp(
                    k[1]["modificationTime"]) + "</span></li>")
            else:
                content["path"].append("<li class='is_list list_content list-group-item'><span class='list name'>" + k[
                    0] + "</span><span class='badge'>" + k[1]["owner"] + "</span><span class='badge'>" + timeStamp(
                    k[1]["modificationTime"]) + "</span></li>")
        return content

    def upload_file(self,request):
        """
        用于接收用户上传文件的请求
        """
        try:
            f = request.files['file']
        except:
            return "Please upload file first!"
        else:
            # 先存入本地然后再存入hdfs
            path = request.form["path"]
            f.save(f.filename)
            try:
                self.this_connection.upload("/lake" + path, "/root/web_app/v4/" + f.filename)
            except:
                os.remove("/root/web_app/v3/" + f.filename)
                return "upload failed~~"
            else:
                # 文件上传成功就返回刷新的地址
                content = self.make_complete_path("/lake" + path)
                os.remove("/root/web_app/v4/" + f.filename)
                return "upload success!", content

    def delete_file_and_mkdir(self,request):
        """
        创建文件夹和删除文件
        """
        req = request.values
        if req["action"] == "delete":
            # 匹配文件名，不允许用户删除不是自己所有的文件
            if req["path"][:7] == "/public":
                file_owner = self.this_connection.status("/lake" + req["path"], True)["owner"]
                if file_owner != self.login_name:
                    return "You can't delete other people's file or directory in public lake",""
                else:
                    self.this_connection.delete("/lake" + req["path"])
                    # 传回修改后刷新的路径
                    content = self.make_complete_path("/lake" + req["previous_path"])
                    return "success deleted", content
            elif req["path"][:4] == "/usr" and req["path"][5:5 + len(self.login_name)] != self.login_name:
                return "You can't delete file or directory in other's lake",""
            else:
                self.this_connection.delete("/lake" + req["path"])
                # 传回修改后刷新的路径
                content = self.make_complete_path("/lake" + req["previous_path"])
                return "success deleted", content

        elif req["action"] == "mkdir":
            if req["path"][5:5 + len(self.login_name)] == self.login_name:
                try:
                    self.this_connection.makedirs("/lake" + req["path"])
                except:
                    return "make directory failed",""
                else:
                    # 传回修改后刷新的路径
                    content = self.make_complete_path("/lake" + req["previous_path"])
                    return "make directory successed", content
            elif req["path"][:7] == "/public":
                try:
                    self.this_connection.makedirs("/lake" + req["path"])
                except:
                    return "make directory failed",""
                else:
                    # 传回修改后刷新的路径
                    content = self.make_complete_path("/lake" + req["path"])
                    return "make directory successed", content
            else:
                return "You can't make directory in other's lake",""




