from flask import redirect, render_template, request, make_response, g, flash, url_for
from flask import Blueprint, session
from functools import wraps

from flask import Blueprint, session, jsonify

import authomatic
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from .models import User

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
            return redirect('/')
        elif result.error:
            raise Exception('FB login failed.')
    return response


@auth_bp.route("/logout",  methods=['GET'])
def logout():
    session.pop('authomatic:fb:state', None)
    #import pdb;pdb.set_trace()
    
    return jsonify({'status':0})

@auth_bp.route('/user-info/', methods=['GET'])
def user_info():
    return jsonify({'id': 10, 'name': 'Vasia', 'surname': 'Pupkin'})

