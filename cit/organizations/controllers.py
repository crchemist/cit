from flask import request, g
from flask import Blueprint, jsonify

from .models import Organization
from ..db import db
from ..utils import login_required, admin_required
import sqlalchemy.exc as sqlalchemy_exc
import sqlalchemy.orm.exc as sqlalchemy_orm_exc

organizations_bp = Blueprint('organizations', __name__)

@organizations_bp.route('/', methods=['POST'])
@admin_required
def organization_create():
    json_req = request.get_json()

    if not json_req:
        return jsonify({'message': 'No input data provided'}), 400

    name = json_req.get('name')
    address = json_req.get('address')
    new_organization = Organization(name, address)
    db.session.add(new_organization)
    db.session.commit()

    return jsonify({'id': new_organization.id}), 201


@organizations_bp.route('/', methods=['GET'])
def organizations_info():
    organization_query = db.session.query(Organization)
    organizations_list = []
    if organization_query:
        organizations_list = \
            [{'id': org.id, 'name': org.name} for org in organization_query]
    return jsonify(organizations=organizations_list)


@organizations_bp.route('/<int:org_id>/add-user/',
                        methods=['POST'])
@login_required
def organization_user_add(org_id):
    user = g.user
    try:
        db.session.begin_nested()
        org = db.session.query(Organization).filter(Organization.id == org_id)
        user.organizations.append(org.first())
        db.session.add(user)
        db.session.commit()
        status = 201
        message = 'user-organization relationship was established'
    except sqlalchemy_exc.IntegrityError:
        db.session.rollback()
        status = 409
        message = 'user-organization relationship was not established ' + \
            'due to the IntegrityError transaction committing.\n' + \
            'Please check whether the specific relationship is' + \
            'already present in database.'
    except sqlalchemy_orm_exc.FlushError:
        db.session.rollback()
        status = 404
        message = 'user-organization relationship was not established ' + \
            'due to the FlushError transaction committing.\n' + \
            'Please check whether the specific organization is' + \
            'present in database.'

    return jsonify({'user_id': user.id, 'org_id': org_id,
                    'message': message}), status
