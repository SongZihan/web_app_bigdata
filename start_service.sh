# 启动uwsgi,需要先创建logs文件夹
uwsgi --ini uwsgi.ini
# 查看状态
ps -ef | grep uwsgi
# 关闭uwsgi
# uwsgi --stop logs/web_app.pid
# 启动nginx,设置了默认启动就不用再开了
systemctl start nginx