from flask import (
    render_template,
    Blueprint,
)

from routes import *

from models.topic import Topic
from models.board import Board
from models.cache import update_created_topic_cache

main = Blueprint('topic', __name__)


@main.route('/<int:id>')
def detail(id):
    m = Topic.get(id)
    u = User.one(id=m.user_id)
    b = m.board()
    token = new_csrf_token()
    return render_template("topic/detail.html", topic=m, user=u, board=b, csrf_token=token)


@main.route("/delete/<int:id>")
@login_required
@csrf_required
def delete(id):
    t = Topic.one(id=id)
    u = current_user()
    if u.id == t.user_id or u.is_admin():
        Topic.delete(id)
    #删除一个人发表的文章后必须更新缓存
    update_created_topic_cache(t.user_id)
    return redirect(url_for('index.index'))


@main.route("/new")
@login_required
def new():
    board_id = int(request.args.get('board_id', -1))
    bs = Board.all()
    token = new_csrf_token()
    return render_template("topic/new.html", bs=bs, csrf_token=token, bid=board_id)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    Topic.new(form, user_id=u.id)
    update_created_topic_cache(u.id)
    return redirect(url_for('index.index'))


@main.route("/edit/<int:id>", methods=['GET', 'POST'])
@login_required
@csrf_required
def edit(id):
    u = current_user()
    t = Topic.one(id=id)

    if u.id == t.user_id or u.is_admin():
        if request.method == 'GET':
            bs = Board.all()
            token = new_csrf_token()
            return render_template("topic/edit.html", topic=t, bs=bs, csrf_token=token, bid=t.board_id)
        else:
            form = request.form
            Topic.update(id, **form)
            update_created_topic_cache(t.id)
            return redirect(url_for('.detail', id=id))
