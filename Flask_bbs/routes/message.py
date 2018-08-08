from flask_mail import Message, Mail
from flask import (
    render_template,
    Blueprint,
)

from routes import *

from models.message import Messages
from secret import admin_mail
from utils import log

main = Blueprint('mail', __name__)
mail = Mail()


@main.route("/add", methods=["POST"])
@login_required
@csrf_required
def add():
    form = request.form.to_dict()
    u = current_user()
    form['sender_id'] = u.id

    r = User.one(username=form['receiver_name'])
    form['receiver_id'] = r.id
    m = Message(
        subject=form['title'],
        body=form['content'],
        sender=admin_mail,
        recipients=[r.email]
    )
    mail.send(m)

    Messages.new(form)
    return redirect(url_for('.index'))


@main.route('/')
@login_required
def index():
    u = current_user()
    token = new_csrf_token()
    sent_mail = Messages.all(sender_id=u.id)
    received_mail = Messages.all(receiver_id=u.id)
    t = render_template(
        'mail/index.html',
        send=sent_mail,
        received=received_mail,
        user=u,
        csrf_token=token
    )
    return t


@main.route('/view/<int:id>')
@login_required
def view(id):
    mail = Messages.one(id=id)
    u = current_user()
    if u.id in [mail.receiver_id, mail.sender_id]:
        return render_template('mail/detail.html', mail=mail, user=u)
    else:
        return redirect(url_for('.index'))
