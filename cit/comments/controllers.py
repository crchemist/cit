from flask import Blueprint
from ..settings import settings

comments_bp = Blueprint(settings['url']['comments_bp'], __name__)