from flask import g
from sqlalchemy_utils import generic_relationship
from geoalchemy2 import Geography
from ..db import db


organization_relationships = db.Table(
    'organization_relationships',
    db.Column('user_id', db.Integer,
              db.ForeignKey('user.id'), nullable=False),
    db.Column('organization_id', db.Integer,
              db.ForeignKey('organization.id'), nullable=False),
    db.PrimaryKeyConstraint('user_id', 'organization_id'))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    organizations = db.relationship('Organization',
                                    secondary=organization_relationships,
                                    backref=db.backref('users',
                                                       lazy='dynamic'))

    fb_first_name = db.Column(db.String(120))
    fb_last_name = db.Column(db.String(120))
    fb_id = db.Column(db.String(40), unique=True)
    email = db.Column(db.String(120), unique=True)
    about_me = db.Column(db.String(120))
    is_superuser = db.Column(db.Boolean, default=False)

    def __init__(self, fb_first_name='', fb_last_name='', fb_id='',
                 email='', about_me='', is_superuser=False):
        self.fb_first_name = fb_first_name
        self.fb_last_name = fb_last_name
        self.fb_id = fb_id
        self.email = email
        self.about_me = about_me
        self.is_superuser = is_superuser

    def __repr__(self):
        return '%s' % self.fb_first_name


class Spatial_ref_sys(db.Model):
    srid = db.Column(db.Integer, primary_key=True)
    auth_name = db.Column(db.String(256))
    auth_srid = db.Column(db.Integer)
    srtext = db.Column(db.String(2048))
    proj4text = db.Column(db.String(2048))


class Vote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    vote = db.Column(db.Boolean)

    # This is used to discriminate between the linked tables.
    target_type = db.Column(db.Unicode(255))

    # This is used to point to the primary key of the linked row.
    target_id = db.Column(db.Integer, nullable=False)

    target = generic_relationship(target_type, target_id)

    author = db.relationship("User")

    def __init__(self, author="", vote="", target=""):
        self.author = author
        self.vote = vote
        self.target = target
