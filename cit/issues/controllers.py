from flask import Blueprint

from .models import Issues
from ..db import db

issues_bp = Blueprint('issues', __name__)