import uuid
from functools import wraps

from flask import (
    session,
    request,
    abort,
    redirect,
    url_for,
)
from models.token import Token
from models.user import User
from utils import log


def current_user():
    uid = session.get('user_id', '')
    u = User.one(id=uid)
    return u


def admin_required(func):
    @wraps(func)  #消除装饰器的不好的副作用
    def wrapper(*args,**kwargs):
        u=current_user()
        if u is not None and u.is_admin():
            return func(*args,**kwargs)
        else:
            abort(401)   #401状态码表示未授权

    return wrapper



#
def login_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if current_user():
            return f(*args, **kwargs)
        else:
            log("login_required")
            return redirect(url_for('index.login_view'))

    return wrapper


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if '_csrf' in request.form:
            token = request.form['_csrf']
        else:
            token = request.args['_csrf']
        u = current_user()
        t = Token.one(content=token)
        log("verify token", t)
        if t is not None and (t.user_id is None or t.user_id == u.id):
            Token.delete(content=token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    if u:
        form = dict(
            content=token,
            user_id=u.id
        )
    else:
        form = dict(
            content=token,
        )
    Token.new(form)
    return token
