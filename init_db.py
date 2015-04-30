# Initialize database.

from cit import create_app
from cit.db import db

app = create_app()
with app.app_context():
    db.create_all()
