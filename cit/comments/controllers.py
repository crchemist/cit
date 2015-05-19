from flask import Blueprint, session, jsonify

from .models import Comment
from ..auth.models import User
from ..db import db

comments_bp = Blueprint('comments', __name__)


class DeleteRequest:
    def delete_comment(self, id):
        comment = Comment.query.get_or_404(int(id))
        permission = User.is_superuser or User.id == Comment.id
        if permission:
            db.session.delete(comment)
        db.session.commit()

    def get_comment(self, id):
        return db.session.query(Comment).get(int(id))


@comments_bp.route('/comments/<comment_id>/', methods=['DELETE'])
def deleted_comment(comment_id):
    dr = DeleteRequest()
    delete = dr.get_comment(comment_id)
    if delete is None:
        response = jsonify({'status': 'Not found'})
        response.status = 404
        return response
    dr.delete_comment(comment_id)
    return jsonify({'status': 'OK'})