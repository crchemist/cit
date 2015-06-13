from flask import redirect, render_template, request, make_response, g
from flask import Blueprint, session, jsonify
from urllib import quote

from .models import Organization
from ..db import db
from ..utils import login_required, admin_required

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
    organization_names = []    
    if organization_query:
        for org in organization_query:            
            organization_dict = {}
            organization_dict.update({
                'id': org.id,
                'name': org.name
                })
            organization_names.append(organization_dict)              
        return jsonify(organizations=organization_names)
    else:
        return jsonify({})


@organizations_bp.route('/organizations/<int:org_id>/add-user/', methods=['POST'])
@login_required
def organization_user_add(org_id):
    user = g.user
    org = db.session.query(Organization).filter(Organization.id == org_id)
    user.organizations.append(org.first())
    db.session.add(user)
    db.session.commit()
    return jsonify({'status': 0}), 201
