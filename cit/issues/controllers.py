from flask import g
from flask import Blueprint, session, jsonify

from ..db import db
from .models import Issue
from ..auth.models import User

issues_bp = Blueprint('issues', __name__)


@issues_bp.route('/issues-info/', methods=['GET', 'POST'])
def issues_info():
    sql_table = db.session.query(Issue, User).join(User)
    execute_table = db.engine.execute(str(sql_table))
    table_dict = []
    for column in execute_table:
        list_row = {}
        list_row.update({
            'id': column.issue_id,
            'reporter': {
                'name': column.user_fb_first_name,
                'surname': column.user_fb_last_name,
                'fb_id': column.user_fb_id
            },
            'description': column.issue_description,
            'coordinates': str(column.issue_coordinates).decode('cp1252')
        })
        table_dict.append(list_row)
    return jsonify(result=table_dict)
