from flask import Flask

import secret
from models.base_model import db

from routes.index import main as index_routes
from routes.topic import main as topic_routes
from routes.reply import main as reply_routes
from routes.board import main as board_routes
from routes.message import main as mail_routes, mail
from routes import current_user
from routes.admin import admin


def configured_app():
    app = Flask(__name__)
    # 设置 secret_key 来使用 flask 自带的 session
    app.secret_key = secret.secret_key

    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:{}@localhost/{}?charset=utf8mb4'.format(
        secret.database_password, secret.database_name
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    mail.init_app(app)
    admin.init_app(app)

    register_routes(app)
    return app


def register_routes(app):
    # 注册蓝图，url_prefix 给路由加前缀
    app.register_blueprint(index_routes)
    app.register_blueprint(topic_routes, url_prefix='/topic')
    app.register_blueprint(reply_routes, url_prefix='/reply')
    app.register_blueprint(board_routes, url_prefix='/board')
    app.register_blueprint(mail_routes, url_prefix='/mail')

    # 注册全局函数
    @app.context_processor
    def utility_processor():
        return dict(current_user=current_user)


if __name__ == '__main__':
    app = configured_app()
    # debug 模式可以自动加载, 修改代码不用重启程序
    # 自动 reload Jinja2
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    config = dict(
        debug=True,
        host='localhost',
        port=2000,
        threaded=True,
    )
    app.run(**config)
