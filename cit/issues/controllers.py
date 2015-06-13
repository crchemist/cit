import os, json
from sqlalchemy import and_
from sqlalchemy.orm import load_only
from flask import g
from ..utils import login_required
from ..db import db
from .models import Issue, Photo
from cit.auth.models import User, Vote
from cit.comments.models import Comment
from flask import Blueprint, request, redirect, url_for, jsonify, current_app, session, jsonify
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from shapely.geos import WKBReader, lgeos
from shapely.geometry import Point

issues_bp = Blueprint('issues', __name__)


@issues_bp.route('/', methods=['GET', 'POST'])
def issues_info():
    issues_user_query = db.session.query(Issue, User)\
        .join(User).all()
    table_dict = []
    for issue, user in issues_user_query:
        list_row = {}
        point = WKBReader(lgeos).read_hex(str(issue.coordinates))
        comments = db.session.query(Comment).filter_by(issue_id=issue.id).all()
        list_of_comments = []

        for comment in comments:
            res = {}
            res['msg'] = comment.message
            res['author_id'] = comment.author_id
            user = db.session.query(User).\
                options(load_only('fb_first_name', 'fb_last_name')).\
                filter_by(id=comment.author_id).first()
            res['author'] = user.fb_first_name + ' ' + user.fb_last_name
            list_of_comments.append(res)

        photos = db.session.query(Photo).filter_by(issue_id=issue.id).all()
        list_of_photos = [photo.file_path for photo in photos]
        list_row.update({
            'type': 'Feature',
            'properties': {
                'id': issue.id,
                'reporter': {
                    'name': user.fb_first_name,
                    'surname': user.fb_last_name,
                    'fb_id': user.fb_id
                },
                'description': issue.description,
                'photos': list_of_photos,
                'comments': list_of_comments
            },
            "geometry": {
                'coordinates': [point.y - 0.00006, point.x + 0.00013],
                'type': 'Point'
            }
        })
        table_dict.append(list_row)

    return jsonify(type='FeatureCollection', features=table_dict,
                   name='Points', keyField='GPSUserName')


@issues_bp.route('/file-upload/', methods=['POST'])
def upload_file():
    error = 0
    file = request.files['file']
    request_data = request.values
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        if request_data.has_key('issue_id'):
            issue = Issue.query.filter_by(id=int(request_data['issue_id'])).\
                first()
            db.session.add(Photo(issue, file_path))
            db.session.commit()
    else:
        filename = ''
        error = 2

    return jsonify({'filename': filename, 'error': error})


@issues_bp.route('/make-issue/', methods=['POST'])
def save_issues():
    request_data = request.get_json()
    issue_description = request_data.get('description')
    issue_coordinates = request_data.get('address')

    if g.user:
        reporter_id = g.user.id
    else:
        reporter_id = None

    new_issue = Issue(issue_description, issue_coordinates, reporter_id)
    db.session.add(new_issue)
    db.session.commit()
    issue_id = new_issue.id

    return jsonify({'issue_id': issue_id})


@issues_bp.route('/<int:issue_id>/vote/', methods=['POST'])
@login_required
def voting(issue_id):
    issue = Issue()
    vote_filter = db.session.query(Vote). \
        filter(and_(Vote.target_id == issue_id, Vote.author_id == g.user.id)
               ).all()
    if vote_filter:
        return jsonify({'msg': 'Already voted'})
    else:
        vote = Vote(author=g.user, vote=True, target=issue)
        vote.target_id = issue_id
        db.session.add(vote)
        db.session.commit()
        return jsonify({}), 201


@issues_bp.route('/<int:issue_id>/unvote/', methods=['DELETE'])
@login_required
def remove_vote(issue_id):
    vote_filter = db.session.query(Vote). \
        filter(and_(Vote.target_id == issue_id, Vote.author_id == g.user.id))
    result = vote_filter.delete(synchronize_session='fetch')
    if result:
        db.session.commit()
        return jsonify({'status': 0})
    else:
        db.session.rollback()
        return jsonify({'msg': 'vote not found', 'status': 1})
