# -*- coding: utf-8 -*-
from application import app
from controllers.login_register import session
@app.before_request
def before_request():


    app.logger.info( "--------before_request--------" )
    return

@app.after_request
def after_request( response ):
    app.logger.info("--------after_request--------")
    return response