# Main init file.
from flask import Flask, render_template, request, g, session

from flask.ext.admin import Admin, BaseView, expose
from flask.ext.admin.contrib.sqla import ModelView

from authomatic.providers import oauth2
from authomatic import Authomatic

from .db import db

from cit.auth.controllers import auth_bp
from cit.issues.controllers import issues_bp
from cit.comments.controllers import comments_bp
from cit.organizations.controllers import organizations_bp
from cit.auth.models import User, Vote
from cit.issues.models import Issue
from cit.comments.models import Comment
from cit.organizations.models import Organization

from mixer.backend.flask import mixer


class AdminView(ModelView):
    @expose('/admin/')
    def is_visible(self):
        if g.user and g.user.is_superuser:
            return True
        return False


def index():
    return render_template('index.html')


def setup_authomatic(app):
    authomatic = Authomatic(
        {'fb': {'consumer_key': app.config['CONSUMER_KEY'],
                'consumer_secret': app.config['CONSUMER_SECRET'],
                'class_': oauth2.Facebook,
                'scope': [], }},
        app.config['SECRET_KEY'], report_errors=False)

    def func():
        g.authomatic = authomatic

    return func


def load_user():
    if 'user_id' not in session.keys():
        g.user = None
    else:
        g.user = User.query.filter_by(id=session['user_id']).first()


def create_app(config='config.ProductionDevelopmentConfig'):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    mixer.init_app(app)

    app.before_request(setup_authomatic(app))
    app.before_request(load_user)

    app.add_url_rule('/', 'index', index)

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(issues_bp, url_prefix='/issues')
    app.register_blueprint(comments_bp, url_prefix='/comments')
    app.register_blueprint(organizations_bp, url_prefix='/organizations')

    admin = Admin(app)

    # add admin views.
    admin.add_view(AdminView(User, db.session))
    admin.add_view(AdminView(Issue, db.session))
    admin.add_view(AdminView(Comment, db.session))
    admin.add_view(AdminView(Organization, db.session))
    admin.add_view(AdminView(Vote, db.session))

    return app
