from flask import Blueprint, session, jsonify, g

from .models import Comment
from ..db import db

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/comments/<int:comment_id>/', methods=['DELETE'])
def delete_comment(comment_id):
    comment_filtered = db.session.query(Comment).filter(Comment.id == comment_id)
    has_permission = g.user.is_superuser or g.user.id == Comment.author_id
    if has_permission:
        result = comment_filtered.delete()
        if result:
            db.session.commit()
            return jsonify({'status': 0})
        else:
            db.session.rollback()
            return jsonify({'msg': 'comment not found', 'status': 1})
    else:
        return jsonify({'status': 1}), 405
