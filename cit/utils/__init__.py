from flask import g
from werkzeug.exceptions import Unauthorized
from functools import wraps


def admin_required(fn):

    def decorated(*args, **kw):
        if not g.user or not g.user.is_superuser:
            raise Unauthorized('Admin permissions required')
        return fn(*args, **kw)

    return decorated


def login_required(fn):

    @wraps(fn)
    def decorated(*args, **kw):
        if not g.user or not (g.user.id or g.user.is_superuser):
            raise Unauthorized('Permission denied')
        return fn(*args, **kw)

    return decorated
