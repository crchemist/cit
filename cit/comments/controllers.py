from flask import Blueprint, request, jsonify, g
from ..utils import login_required

from .models import Comment
from ..issues.models import Issue
from ..auth.models import User
from ..db import db

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/', methods=['POST'])
@login_required
def comment_add():
    comment_id = 0
    error = 400
    json_req = request.get_json()
    if json_req:
        comment = Comment(author=g.user, issue_id=json_req.get('issue_id'),
                          message=json_req.get('msg'))
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id
        error = 201
    return jsonify({'id': comment_id}), error


@comments_bp.route('/comments/<int:comment_id>/', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    comment_query = db.session.query(Comment)
    comment_filtered = comment_query.filter(Comment.id == comment_id)
    result = comment_filtered.delete(synchronize_session='fetch')
    if result:
        db.session.commit()
        return jsonify({'status': 0})
    else:
        db.session.rollback()
        return jsonify({'msg': 'comment not found', 'status': 1})
