# 绝对链接管理器
from application import app

import os


class UrlManager(object):
    @staticmethod
    def buildUrl(path):
        config_domain = app.config['DOMAIN']
        return "%s%s" % (config_domain['www'], path)

    @staticmethod
    def buildStaticUrl(path):
        path = "/static" + path
        return UrlManager.buildUrl(path)
