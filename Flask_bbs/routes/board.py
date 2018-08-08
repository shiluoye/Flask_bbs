from flask import (
    render_template,
    Blueprint,
)

from routes import *

from models.board import Board

main = Blueprint('board', __name__)


@main.route("/admin")
@admin_required
def index():
    return render_template('board/admin_index.html')


@main.route("/add", methods=["POST"])
@admin_required
def add():
    form = request.form

    Board.new(form)
    return redirect(url_for('.index'))
