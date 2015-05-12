from flask import g
from flask import Blueprint, session, jsonify

from ..db import db

issues_bp = Blueprint('issues-path', __name__)

@issues_bp.route('/issues-info/', methods=['GET'])
def issues_info():
	if g.issues:
		reporter_result = {}
		if g.user:
			reporter_result = {'fb_id': g.user.fb_id, 'name': g.user.fb_first_name, 'surname': g.user.fb_last_name}
		result = {'id': g.issues.id, 'reporter': reporter_result, 'description': g.issues.description, 'coordinates': str(g.issues.coordinates)}
	return jsonify(result)