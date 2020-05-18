# 绝对链接管理器
from flask import url_for

from application import app

import os


class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        config_domain = app.config['DOMAIN']
        return "%s%s" % (config_domain['www'], path)

    @staticmethod
    def buildStaticUrl(path):
        # 改进版,解决了domain为公网ip时无法访问static文件的问题
        return url_for('static', filename=path)
