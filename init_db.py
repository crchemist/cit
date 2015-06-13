# Initialize database.
from cit import create_app
from cit.db import db
from mixer.backend.sqlalchemy import Mixer
from mixer.backend.flask import mixer
from cit.auth.models import User
from cit.organizations.models import Organization
from cit.issues.models import Issue, Photo
from cit.comments.models import Comment
import sys
import argparse


class MyOwnMixer(Mixer):
    def populate_target(self, values):
        target = self.__scheme(**values)
        return target

mixer = MyOwnMixer()


class InitDB():
    def __init__(self, app):
        self.app = app

    def create_parser(self):
        parser = argparse.ArgumentParser()
        parser.add_argument('--make-admin', action='store', default='')
        args = parser.parse_args()

        return parser

    def generate_test_data(self):
        with self.app.app_context():
            organization = mixer.blend(Organization,
                                       name=mixer.RANDOM,
                                       address='POINT(49.836134 24.023151)')
            db.session.add(organization)
            user = mixer.blend(User,
                               fb_first_name=mixer.RANDOM,
                               fb_last_name=mixer.RANDOM,
                               fb_id=mixer.RANDOM,
                               email=mixer.RANDOM,
                               about_me=mixer.RANDOM)
            user = User(user.fb_first_name, user.fb_last_name, user.fb_id,
                        user.email, user.about_me)
            user.organizations.append(organization)
            db.session.add(user)
            db.session.commit()
            issue = mixer.blend(Issue,
                                reporter='1',
                                description=mixer.RANDOM,
                                coordinates='POINT(49.839357 24.028398)')
            db.session.add(issue)
            comment = mixer.blend(Comment,
                                  author=user,
                                  issue=issue,
                                  message=mixer.RANDOM)
            db.session.add(comment)
            photo = mixer.blend(Photo,
                                issue=issue,
                                file_path=mixer.RANDOM)
            db.session.add(photo)
            db.session.commit()

    def make_user_as_admin(self, user_id):
        with self.app.app_context():
            db.session.query(User).filter(User.fb_id == user_id).\
                update({'is_superuser': True})
            db.session.commit()


if __name__ == '__main__':
    app = create_app()
    init_db = InitDB(app)
    parser = init_db.create_parser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.make_admin:
        init_db.make_user_as_admin(namespace.make_admin)
    else:
        init_db.generate_test_data()
