import os
from flask import Blueprint, request, redirect, url_for
from werkzeug import secure_filename
from werkzeug.datastructures import FileStorage

issues_bp = Blueprint('issues', __name__)

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'media')

@issues_bp.route('/file-upload/', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file:
    	filename = secure_filename(file.filename)
    	file.save(os.path.join(UPLOAD_FOLDER, filename))
    
	return redirect('/')