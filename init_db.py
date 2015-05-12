# Initialize database.
 
from cit import create_app
from cit.db import db
from mixer.backend.sqlalchemy import Mixer
from mixer.backend.flask import mixer
from cit.auth.models import User
from cit.issues.models import Issues
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
        issues = mixer.blend(Issues, reporter="1", description=mixer.RANDOM, coordinates='POINT(49 22)')
        db.session.add(issues)
        db.session.commit()
 
 
if __name__ == "__main__":
    parser = createParser()
    namespace = parser.parse_args(sys.argv[1:])
 
    print (namespace)
 
    if namespace.init_data:
        generate_test_data()
