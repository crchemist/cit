from flask import Flask, render_template, request, g

from flask.ext.admin import Admin, BaseView, expose

from .db import db

from cit.auth.controllers import auth_bp

class AdminPageView(BaseView):
    @expose('/')
    def index(self): 
        return self.render('index2.html') 

def index():
    return render_template('index.html')

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')
    db.init_app(app)

    app.add_url_rule('/', 'index', index)

    app.register_blueprint(auth_bp, url_prefix='/auth')

    admin = Admin(app)
    return app
