# Main init file.
from flask import Flask, render_template, request, g, session

from flask.ext.admin import Admin, BaseView
from flask.ext.admin.contrib.sqla import ModelView

from authomatic.providers import oauth2
from authomatic import Authomatic

from .db import db

from cit.auth.controllers import auth_bp
from cit.issues.controllers import issues_bp
from cit.auth.models import User
from cit.issues.models import Issues
from mixer.backend.flask import mixer


def index():
    return render_template('index.html')


def setup_authomatic(app):
    authomatic = Authomatic(
        {'fb': {'consumer_key': app.config['CONSUMER_KEY'],
                'consumer_secret': app.config['CONSUMER_SECRET'],
                'class_': oauth2.Facebook,
                'scope': [], }},
        '5ecRe$', report_errors=False)

    def func():
        g.authomatic = authomatic

    return func


def load_user():
    if 'user_id' not in session.keys():
        g.user = None
    else:
        g.user = User.query.filter_by(id=session['user_id']).first()


def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    db.init_app(app)

    mixer.init_app(app)

    app.before_request(setup_authomatic(app))
    app.before_request(load_user)

    app.add_url_rule('/', 'index', index)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(issues_bp, url_prefix='/issues')

    admin = Admin(app)

    # add admin views.
    admin.add_view(ModelView(User, db.session))

    return app