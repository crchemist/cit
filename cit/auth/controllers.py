from flask import redirect, render_template, request, make_response, g
from flask import Blueprint, session, url_for, redirect_template

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
    errorMessage = None
    if result:
        if result.user:
            return redirect(url_for('login/fb'))
        elif result.error:
        	errorMessage = 'Facebook login failed.'
		return redirect_template('/templates/index.html',error = errorMessage)
    else:
	errorMessage = 'Facebook login failed.'
        return redirect_template('/templates/index.html',error = errorMessage)     	
    return response
