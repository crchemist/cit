from flask import Blueprint, session, jsonify

from .models import Comment
from ..auth.models import User
from ..db import db

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/comments/<int:comment_id>/', methods=['DELETE'])
def delete_comment(comment_id):
    comment_query = db.session.query(Comment)
    comment_filtered = comment_query.filter(Comment.id == comment_id)
    permission = User.is_superuser or User.id == Comment.id
    if permission:
        comment_filtered.delete()
        db.session.commit()
        return jsonify({'status': 'OK'})