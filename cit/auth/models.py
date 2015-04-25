from flask import g

from ..db import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True)
    fb_access_token = db.Column(db.String(120), unique=True)
    fb_id = db.Column(db.Integer, unique=True)

    def __init__(self, email, fb_access_token, fb_id):
        self.email = email
        self.fb_access_token = fb_access_token
        self.fb_id = fb_id

    def __repr__(self):
        return '<User %r>' % self.email

