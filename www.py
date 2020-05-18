# -*- coding: utf-8 -*-
from application import app
from controllers.login_register import login_page
from controllers.user_ui import user_page

# from flask_debugtoolbar import DebugToolbarExtension
# toolbar = DebugToolbarExtension( app )

'''
拦截器处理 和 错误处理器
'''
# from interceptors.Auth import *
from interceptors.errorHandler import *

app.register_blueprint(login_page, url_prefix="/")
app.register_blueprint(user_page, url_prefix="/user")

'''
模板函数
'''
from common.libs.UrlManager import UrlManager

app.add_template_global(UrlManager.buildStaticUrl, 'buildStaticUrl')
app.add_template_global(UrlManager.buildUrl, 'buildUrl')
