from ..db import db
from ..auth.models import User
from geoalchemy2 import Geography

class Issues(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	reporter = db.Column(db.Integer, db.ForeignKey("user.id"))
	description = db.Column(db.String(120))
	coordinates = db.Column(db.Geography(geometry_type='POINT'))

	def __init__(self, description = "", coordinates = ""):
		self.description = description
		self.coordinates = coordinates