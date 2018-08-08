from sqlalchemy import create_engine

import secret
from app import configured_app
from models.base_model import db
from models.board import Board
from models.reply import Reply
from models.topic import Topic
from models.user import User
from models.token import Token


def reset_database():
    url = 'mysql+pymysql://root:{}@localhost/?charset=utf8mb4'.format(secret.database_password)
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS {}'.format(secret.database_name))
        c.execute('CREATE DATABASE {} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci'.format(secret.database_name))
        c.execute('USE {}'.format(secret.database_name))

    db.metadata.create_all(bind=e)


def generate_fake_date():
    form = dict(
        username='test',
        password='123',
        re_password='123',
        role='admin'
    )
    u = User.register(form)
    boards = ['分享', '问答', '招聘', '客户端测试']
    for board in boards:
        form = dict(
            title=board
        )
        Board.new(form)
    with open('markdown_demo.md', encoding='utf8') as f:
        content = f.read()
    topic_form = dict(
        title='markdown demo',
        board_id=1,
        content=content
    )
    Topic.new(topic_form, u.id)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
        generate_fake_date()
