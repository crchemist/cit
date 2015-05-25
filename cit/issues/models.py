from ..db import db
from geoalchemy2 import Geography


class Issue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    reporter = db.Column(db.Integer, db.ForeignKey("user.id"))
    description = db.Column(db.String(120))
    coordinates = db.Column(Geography(geometry_type='GEOMETRY'))

    def __init__(self, description="", coordinates="", reporter=None):
        self.description = description
        self.coordinates = coordinates
        self.reporter = reporter
