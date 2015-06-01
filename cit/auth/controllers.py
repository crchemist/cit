from flask import redirect, render_template, request, make_response, g
from flask import Blueprint, session, jsonify
from urllib import quote

import authomatic
from authomatic.adapters import WerkzeugAdapter
from authomatic import Authomatic

from .models import User, Organization
from ..db import db
from ..utils import owner_required

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
                db.create_all()
                db.session.add(User(result.user.first_name, result.user.last_name, result.user.id, result.user.email))
                db.session.commit()
                user = User.query.filter_by(fb_id=result.user.id).first()
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
            {'id': g.user.id, 'first_name': g.user.fb_first_name, 'last_name': g.user.fb_last_name,
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


@auth_bp.route('/organizations/', methods=['POST'])
def organization_update():
    json_req = request.get_json()

    if not json_req:
        return jsonify({'message': 'No input data provided'}), 400

    name = json_req.get('name')
    address = json_req.get('address')
    new_organization = Organization(name, address)
    db.session.add(new_organization)
    db.session.commit()

    return jsonify({'id': new_organization.id}), 201


@auth_bp.route('/organizations/', methods=['GET'])
def organizations_info():
    organization_query = db.session.query(Organization)
    organization_dict = {}
    organization_names = []
    if organization_query:
        for org in organization_query:
            organization_names.append(org.name)
            organization_dict['name'] = sorted(organization_names)
        return jsonify(organization_dict)
    else:
        return jsonify({})


@auth_bp.route('/organizations/<int:org_id>/add-user/', methods=['POST'])
@owner_required
def organization_user_add(org_id):
    user = g.user
    org = db.session.query(Organization).filter(Organization.id == org_id)
    user.organizations.append(org.first())
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 0}), 201
