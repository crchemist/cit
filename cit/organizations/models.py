from flask import g
from geoalchemy2 import Geography
from ..db import db


class Organization(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120))
    address = db.Column(Geography(geometry_type='GEOMETRY'))

    def __init__(self, name="", address=""):
        self.name = name
        self.address = address

    def __repr__(self):
        return '%s' % self.name
