from flask import redirect, render_template, request, make_response, g, flash
from flask import Blueprint

import authomatic
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/fb/', methods=['GET', 'POST'])
def login():
    response = make_response()
    result = g.authomatic.login(WerkzeugAdapter(request, response), 'fb')
    if result:
        if result.user:
		return redirect('#/?msg={}'.format(urlquote('')))
        elif result.error:
		return redirect('#/?msg={}'.format(urlquote('Facebook login failed.')))
            	#raise Exception('FB login failed.')
    return response
