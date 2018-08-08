import os
import uuid

from flask import (
    render_template,
    request,
    redirect,
    session,
    url_for,
    Blueprint,
    abort,
    send_from_directory
)

from models.board import Board
from models.topic import Topic
from models.user import User
from models.cache import created_topic, replied_topic
from routes import (
    current_user,
    new_csrf_token,
    csrf_required,
    login_required
)
from utils import log

main = Blueprint('index', __name__)

"""
主页路由
    访问首页
    注册
    登录
    头像
"""


@main.route("/")
def index():
    board_id = int(request.args.get('board_id', -1))
    if board_id == -1:
        ms = Topic.all()
    else:
        ms = Topic.all(board_id=board_id)

    ms.sort(key=lambda x: x.created_time, reverse=True)
    bs = Board.all()
    u = current_user()
    return render_template("topic/index.html", user=u, ms=ms, bs=bs, bid=board_id)


@main.route("/about")
def about():
    u = current_user()
    return render_template('about.html', user=u)


@main.route("/register", methods=['POST'])
@csrf_required
def register():
    form = request.form.to_dict()
    u = User.register(form)
    if u is None:
        result = False
    else:
        result = True
    return redirect(url_for('.register_view', success=result))


@main.route("/register/view")
def register_view():
    token = new_csrf_token()
    success = request.args.get('success')
    return render_template('sign/signup.html', success=success, csrf_token=token)


@main.route("/login", methods=['POST'])
@csrf_required
def login():
    form = request.form
    u = User.validate_login(form)
    if u is None:
        return redirect(url_for('.login_view', success=False))
    else:
        # session 中写入 user_id
        session['user_id'] = u.id
        # 设置 cookie 有效期为 永久
        session.permanent = True
        return redirect(url_for('.index'))


@main.route("/login/view")
def login_view():
    token = new_csrf_token()
    success = request.args.get('success')
    return render_template('sign/signin.html', success=success, csrf_token=token)


@main.route("/signout")
@login_required
def signout():
    session.pop('user_id')
    return redirect(url_for('.index'))


@main.route('/profile')
@login_required
def profile():
    u = current_user()
    token = new_csrf_token()
    return render_template('user/profile.html', user=u, csrf_token=token)


@main.route('/setting', methods=['POST'])
@csrf_required
def setting():
    form = request.form.to_dict()
    u = current_user()
    if 'new_pass' in form:
        old = form['old_pass']
        new = form['new_pass']
        if u.password == User.salted_password(old):
            User.update(u.id, password=User.salted_password(new))
        else:
            log('旧密码错误')
    else:
        User.update(u.id, signature=form['signature'])
    return redirect(url_for('.profile'))


@main.route('/user/<int:id>')
def user_detail(id):
    u = User.one(id=id)
    if u is None:
        abort(404)
    else:
        # created = Topic.created_topic(user_id=u.id)
        # replied = Topic.replied_topic(user_id=u.id)

        # 用 Redis 缓存
        created = created_topic(u.id)
        replied = replied_topic(u.id)
        return render_template(
            'user/index.html',
            user=u,
            created=created,
            replied=replied
        )


@main.route('/image/add', methods=['POST'])
@csrf_required
def avatar_add():
    file = request.files['avatar']

    suffix = file.filename.split('.')[-1]
    filename = '{}.{}'.format(str(uuid.uuid4()), suffix)
    path = os.path.join('images', filename)
    file.save(path)

    u = current_user()
    User.update(u.id, image='/images/{}'.format(filename))

    return redirect(url_for('.profile'))


@main.route('/images/<filename>')
def image(filename):
    # 不要直接拼接路由，不安全，比如
    # open(os.path.join('images', filename), 'rb').read()
    return send_from_directory('images', filename)
