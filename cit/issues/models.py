from ..db import db
from ..auth.models import User
#from geoalchemy2 import Geometry

class Issues(db.Model):
	reporter = db.Column(db.Integer, db.ForeignKey("user.id"))
	description = db.Column(db.String(120))
	coordinates = db.Column(db.String(120))

	def __init__(self, description = "", coordinates = ""):
		self.description = description
		self.coordinates = coordinates