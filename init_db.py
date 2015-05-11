# Initialize database.
 
from cit import create_app
from cit.db import db
from mixer.backend.sqlalchemy import Mixer
from mixer.backend.flask import mixer
from cit.auth.models import User
import sys
import argparse
from sqlalchemy import update
 
 
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
                           fb_first_name=mixer.RANDOM,
                           fb_last_name=mixer.RANDOM,
                           fb_id=mixer.RANDOM,
                           email=mixer.RANDOM)
        db.session.add(user)
        db.session.commit()
 
 
if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
 
    print (namespace)
 
    if namespace.init_data:
        generate_test_data()

    if namespace.make_admin:
        generate_test_data()
