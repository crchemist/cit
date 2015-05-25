# Initialize database.
from sqlalchemy import update
from cit import create_app
from cit.db import db
from mixer.backend.sqlalchemy import Mixer
from mixer.backend.flask import mixer
from cit.auth.models import User
from cit.auth.models import Organization
from cit.issues.models import Issue
from cit.comments.models import Comment
from random import randint
import sys
import argparse

app = create_app()
with app.app_context():
    db.create_all()


# Generate a random user by calling argument "--init-data"


class MyOwnMixer(Mixer):
    def populate_target(self, values):
        target = self.__scheme(**values)
        return target


mixer = MyOwnMixer()


def createParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--init-data', action='store_true')
    parser.add_argument('--make-admin', action='store', default='')
    args = parser.parse_args()

    return parser


def generate_test_data():
    with app.app_context():
        user = mixer.blend(User,
                           organization='1',
                           fb_first_name=mixer.RANDOM,
                           fb_last_name=mixer.RANDOM,
                           fb_id=mixer.RANDOM,
                           email=mixer.RANDOM,
                           about_me=mixer.RANDOM)
        db.session.add(user)
        issue = mixer.blend(Issue,
                            reporter='1',
                            description=mixer.RANDOM,
                            coordinates='POINT(49 22)')
        db.session.add(issue)
        comment = mixer.blend(Comment,
                              author_id='1',
                              issue_id='1',
                              message=mixer.RANDOM)
        db.session.add(comment)
        organization = mixer.blend(Organization,
                            name=mixer.RANDOM,
                            address='POINT(77 77)')
        db.session.add(organization)
        db.session.commit()


def make_user_as_admin(user_id):
    with app.app_context():
        db.session.query(User).filter(User.fb_id == user_id).update({"is_superuser": True})
        db.session.commit()


if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])

    if namespace.init_data:
        generate_test_data()
    if namespace.make_admin:
        make_user_as_admin(namespace.make_admin)
        