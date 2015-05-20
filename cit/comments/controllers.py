from flask import Blueprint, request, jsonify
from .models import Comment
from ..db import db

comments_bp = Blueprint('comments', __name__)


@comments_bp.route('/', methods=['POST'])
def comments_add():
    comment_id = 0
    error = 400
    json_req = request.get_json()
    if json_req:
        db.create_all()
        comment = Comment(json_req.get('msg'))
        db.session.add(comment)
        db.session.commit()
        comment_id = comment.id
        error = 201
    return jsonify({'id': comment_id}), error