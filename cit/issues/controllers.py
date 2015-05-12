from flask import g
from flask import Blueprint, session, jsonify

#from .models import Issues
from ..auth.models import User
from ..db import db

issues_bp = Blueprint('issues-path', __name__)

@issues_bp.route('/issues-info/', methods=['GET'])
def issues_info():
	res2 = ({'fb_id': g.issues.description, 'name': g.issues.description, 'surname': g.issues.description})
	res = ({'id': g.issues.id, 'reporter': res2, 'description': g.issues.description})
	return jsonify(res)