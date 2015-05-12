import os
from flask import Blueprint, request, redirect, url_for, jsonify, current_app
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage

issues_bp = Blueprint('issues', __name__)

@issues_bp.route('/file-upload/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))

    return jsonify({'filename': filename})