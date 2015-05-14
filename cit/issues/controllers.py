from flask import Blueprint
from ..db import db
from .models import Issue
from ..auth.models import User
from shapely.geos import WKBReader, lgeos

issues_bp = Blueprint('issues', __name__)


@issues_bp.route('/', methods=['GET', 'POST'])
def issues_info():
    issues_user_query = db.session.query(Issue, User).join(User).all()
    table_dict = []
    for issue, user in issues_user_query:
        list_row = {}
        list_row.update({
            'id': issue.id,
            'reporter': {
                'name': user.fb_first_name,
                'surname': user.fb_last_name,
                'fb_id': user.fb_id
            },
            'description': issue.description,
            'coordinates': str(WKBReader(lgeos).read_hex(str(issue.coordinates)))
        })
        table_dict.append(list_row)
    return jsonify(result=table_dict)
