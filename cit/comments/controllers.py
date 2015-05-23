from flask import Blueprint, request, jsonify, g
from sqlalchemy import or_

from .models import Comment
from ..issues.models import Issue
from ..auth.models import User
from ..db import db

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/', methods=['POST'])
def comment_add():
    comment_id = 0
    error = 400
    json_req = request.get_json()
    if json_req:
        issue = Issue.query.filter_by(id=json_req.get('issue_id')).first()
        comment = Comment(author=g.user, issue=issue, message=json_req.get('msg'))
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id
        error = 201
    return jsonify({'id': comment_id}), error


@comments_bp.route('/comments/<int:comment_id>/', methods=['DELETE'])
def delete_comment(comment_id):
    comment_query = db.session.query(Comment)
    user_sq = comment_query.join(User).filter(Comment.author_id == User.id).\
        filter(Comment.author_id == g.user.id).subquery()
    filter_user = comment_query.filter(or_(g.user.is_superuser is True, user_sq))
    comment_filtered = filter_user.filter(Comment.id == comment_id)
    result = comment_filtered.delete(synchronize_session='fetch')
    if result:
        db.session.commit()
        return jsonify({'status': 0})
    else:
        db.session.rollback()
        return jsonify({'msg': 'comment not found', 'status': 1})
