from flask import g
from geoalchemy2 import Geography
from ..db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organization = db.Column(db.Integer, db.ForeignKey("organization.id"))
    fb_first_name = db.Column(db.String(120))
    fb_last_name = db.Column(db.String(120))
    fb_id = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(120), unique=True)
    about_me = db.Column(db.String(120))
    is_superuser = db.Column(db.Boolean, default=False)

    def __init__(self, fb_first_name="", fb_last_name="", fb_id="", email="", about_me="", is_superuser=False):
        self.fb_first_name = fb_first_name
        self.fb_last_name = fb_last_name
        self.fb_id = fb_id
        self.email = email
        self.about_me = about_me
        self.is_superuser = is_superuser

    def __repr__(self):
        return '<User %r>' % self.email


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(120))
    address = db.Column(Geography(geometry_type='GEOMETRY'))

    def __init__(self, name="", address=""):
        self.name = name
        self.address = address