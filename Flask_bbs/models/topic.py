from sqlalchemy import Integer, Column, UnicodeText, Unicode, desc

from models.base_model import SQLMixin, db
from models.board import Board
from models.reply import Reply
from models.user import User


class Topic(SQLMixin, db.Model):
    views = Column(Integer, nullable=False, default=0)
    title = Column(Unicode(50), nullable=False)
    content = Column(UnicodeText, nullable=False)
    user_id = Column(Integer, nullable=False)
    board_id = Column(Integer, nullable=False)

    @classmethod
    def new(cls, form, user_id):
        form['user_id'] = user_id
        m = super().new(form)
        return m

    @classmethod
    def get(cls, id):
        m = cls.one(id=id)
        m.views += 1
        m.save()
        return m

    @classmethod
    def delete(cls, id):
        super().delete(id=id)
        Reply.delete(topic_id=id)

    @classmethod
    def created_topic(cls, user_id):
        topics = cls.query.filter_by(user_id=user_id).order_by(desc(cls.created_time)).all()
        return topics

    # 这里可以使用静态方法，返回找到的对象，因为这个方法只会被一个类调用，也就是topic
    @staticmethod
    def replied_topic(cls, user_id):
        replies = Reply.query.filter_by(user_id=user_id).order_by(Reply.created_time).all()
        topic_ids = []
        for reply in replies:
            if reply.topic_id not in topic_ids:
                topic_ids.append(reply.topic_id)
        replied_topics = [Topic.one(id) for id in topic_ids]
        return replied_topics

    def user(self):
        user = User.one(id=self.user_id)
        return user

    def board(self):
        b = Board.one(id=self.board_id)
        return b

    def replies(self):
        replies = Reply.all(topic_id=self.id)
        return replies

    def reply_count(self):
        count = len(self.replies())
        return count

    def last_reply(self):
        last_reply = Reply.query.filter_by(topic_id=self.id).order_by(desc(Reply.created_time)).limit(1).first()
        return last_reply
