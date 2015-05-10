from ..db import db
#from geoalchemy2 import Geometry

class Issues(db.Model):
	#reporter = db.Column(db.Integer, ForeignKey("User.id"))
	description = db.Column(db.String(120))
	coordinates = db.Column(db.String(120))

	def __init__(self, description = "", coordinates = ""):
		self.description = description
		self.coordinates = coordinates