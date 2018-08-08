from flask import (
    Blueprint,
)

from routes import *

from models.message import Messages
from models.cache import update_replied_topic_cache

from models.reply import Reply
from utils import log

main = Blueprint('reply', __name__)


def users_from_content(content):
    # 内容 @123 内容
    # 如果用户名含有空格 就不行了 @name 123
    # 'a b c' -> ['a', 'b', 'c']
    parts = content.split()
    users = []

    for p in parts:
        if p.startswith('@'):
            username = p[1:]
            u = User.one(username=username)
            log('users_from_content <{}> <{}> <{}>'.format(username, p, parts))
            if u is not None:
                users.append(u)

    return users


def send_mails(sender, receivers, content):
    log('send_mail', sender, receivers, content)
    for r in receivers:
        form = dict(
            title='你被 {} @ 了'.format(sender.username),
            content=content,
            sender_id=sender.id,
            receiver_id=r.id
        )
        Messages.new(form)


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form
    u = current_user()

    content = form['content']
    users = users_from_content(content)
    send_mails(u, users, content)
    form = form.to_dict()
    m = Reply.new(form, user_id=u.id)
    update_replied_topic_cache(u.id)
    return redirect(url_for('topic.detail', id=m.topic_id))
