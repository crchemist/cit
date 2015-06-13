from flask import redirect, render_template, request, make_response, g
from flask import Blueprint, session, jsonify
from urllib import quote

import authomatic
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from .models import User
from ..db import db

auth_bp = Blueprint('auth', __name__)


def _session_saver():
    session.modified = True


@auth_bp.route('/login/fb/', methods=['GET', 'POST'])
def login():
    response = make_response()
    result = g.authomatic.login(WerkzeugAdapter(request, response), 'fb',
                                session=session,
                                session_saver=_session_saver)
    if result:
        if result.user:
            result.user.update()
            user = User.query.filter_by(fb_id=result.user.id).first()
            if not user:
                user = User(result.user.first_name,
                                    result.user.last_name,
                                    result.user.id,
                                    result.user.email)
                db.session.add(user)
                db.session.flush()
                db.session.commit()
            session['user_id'] = user.id
            return redirect('/')

        elif result.error:
            redirect_path = '#/?msg={}'.format(quote('Facebook login failed.'))
            return redirect(redirect_path)
    return response


@auth_bp.route('/user-info/', methods=['GET'])
def user_info():
    res = {}
    if g.user:
        res = (
            {'id': g.user.id, 'first_name': g.user.fb_first_name,
             'last_name': g.user.fb_last_name,
             'fb_id': g.user.fb_id,
             'email': g.user.email})
    return jsonify(res)


@auth_bp.route('/logout/', methods=['GET'])
def logout():
    session.pop('authomatic:fb:state', None)
    session.pop('user_id', None)
    return jsonify({'status': 0})


@auth_bp.route('/user/profile/', methods=['POST'])
def profile_update():
    json_req = request.get_json()
    if not json_req:
        return jsonify({'message': 'No input data provided'}), 400
    user_query = db.session.query(User)
    user_filtered = user_query.filter(User.id == g.user.id)
    user_filtered.update({'fb_first_name': json_req.get('name'),
                          'fb_last_name': json_req.get('surname')})
    db.session.commit()
    return jsonify({}), 201
