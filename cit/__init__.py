from flask import Flask, render_template, request, g
from flask.ext.admin import Admin, BaseView, expose

from authomatic.providers import oauth2
from authomatic import Authomatic

from .db import db

from cit.auth.controllers import auth_bp


class AdminPageView(BaseView):
    @expose('/')
    def index(self): 
        return self.render('index2.html') 

def index():
    return render_template('index.html')

def setup_authomatic(app):
    authomatic = Authomatic(
        {'fb': {'consumer_key': app.config['CONSUMER_KEY'],
                'consumer_secret': app.config['CONSUMER_SECRET'],
                'class_': oauth2.Facebook,
                'scope': [],}},
        '5ecRe$', report_errors=False)
    def func():
        g.authomatic = authomatic
    return func

def create_app():
    app = Flask(__name__)
    global app
    app.config.from_object('config')

    db.init_app(app)
    app.before_request(setup_authomatic(app))

    app.add_url_rule('/', 'index', index)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    admin = Admin(app)
    return app
