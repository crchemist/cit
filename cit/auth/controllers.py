from flask import Flask, render_template, request, make_response
from flask import Blueprint

import authomatic
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from .models import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login/fb/', methods=['GET', 'POST'])
def login():
    response = make_response()
    result = authomatic.login(WerkzeugAdapter(request, response), 'fb')
