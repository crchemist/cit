from flask import Blueprint
from ..settings import settings

issues_bp = Blueprint(settings['url']['issues_bp'], __name__)