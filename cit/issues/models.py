from ..db import db
from geoalchemy2 import Geography


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.Integer, db.ForeignKey('user.id'))
    description = db.Column(db.String(120))
    coordinates = db.Column(Geography(geometry_type='GEOMETRY'))

    def __init__(self, description='', coordinates='', reporter=None):
        self.description = description
        self.coordinates = coordinates
        self.reporter = reporter

    def __repr__(self):
        return '%s' % self.description


class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    issue_id = db.Column(db.Integer, db.ForeignKey('issue.id'))
    file_path = db.Column(db.String(200))

    issue = db.relationship('Issue')

    def __init__(self, issue='', file_path=''):
        self.issue = issue
        self.file_path = file_path
