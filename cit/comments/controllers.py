from flask import Blueprint, request, jsonify, g
from ..utils import login_required

from .models import Comment
from ..db import db

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/', methods=['POST'])
@login_required
def comment_add():
    comment_id = 0
    status = 400

    if request.form['issue_id'] and request.form['msg']:
        comment = Comment(author_id=g.user.id,
                          issue_id=request.form['issue_id'],
                          message=request.form['msg'])
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id
        status = 201
    return jsonify({'id': comment_id}), status


@comments_bp.route('/<int:comment_id>/', methods=['DELETE'])
@login_required
def delete_comment(comment_id):
    db.session.begin_nested()
    comment_query = db.session.query(Comment)
    comment_filtered = comment_query.filter(Comment.id == comment_id)
    result = comment_filtered.delete(synchronize_session='fetch')
    if result:
        db.session.commit()
        status = 204
        message = 'comment was successfully deleted'
    else:
        db.session.rollback()
        status = 404
        message = 'comment not found'

    return jsonify({'msg': message}), status
