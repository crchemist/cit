# Import flask and template operators
from flask import Flask, render_template, request, g

# Import SQLAlchemy
from flask.ext.sqlalchemy import SQLAlchemy

# Define the WSGI application object
app = Flask(__name__)

# Configurations
app.config.from_object('config')

# Define the database object which is imported
# by modules and controllers
db = SQLAlchemy(app)

#import pdb;pdb.set_trace()
@app.route('/')
def index():
    return render_template('index.html',site_title=app.config["SITE_TITLE"])
