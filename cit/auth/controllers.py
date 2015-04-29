from flask import redirect, render_template, request, make_response, g
from flask import Blueprint, session, jsonify
from urllib import quote

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
            redirect_path = '#/?msg={}'.format(quote('Facebook login failed.'))
            return redirect(redirect_path )
    
    return response

@auth_bp.route('/user-info/', methods=['GET'])
def user_info():
    return jsonify({'id': 10, 'name': 'Vasia', 'surname': 'Pupkin'})
