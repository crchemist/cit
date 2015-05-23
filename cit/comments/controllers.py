from flask import Blueprint, request, jsonify, g
from .models import Comment
from ..issues.models import Issue
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