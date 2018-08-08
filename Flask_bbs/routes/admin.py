from flask import abort
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView

from models.base_model import db
from models.user import User
from models.topic import Topic
from models.reply import Reply
from models.board import Board

from models.cache import update_created_topic_cache, update_replied_topic_cache

from routes import current_user, login_required


# Create customized model view class
class BaseModelView(ModelView):
    column_display_pk = True

    def is_accessible(self):
        u = current_user()
        if u:
            return u.is_admin()
        else:
            return False


class UserModelView(BaseModelView):

    def delete_model(self, model):
        ts = Topic.all(user_id=model.id)
        for t in ts:
            Topic.delete(t.id)
        Reply.delete(user_id=model.id)
        User.delete(id=model.id)
        return True


class TopicModelView(BaseModelView):

    def delete_model(self, model):
        # 先保存 replier id，Topic删除后就拿不到了
        rs = model.replies()
        rs_id = set([r.user_id for r in rs])

        Topic.delete(id=model.id)
        update_created_topic_cache(user_id=model.user_id)

        for _id in rs_id:
            update_replied_topic_cache(user_id=_id)
        return True


class BoardModelView(BaseModelView):
    can_delete = False


# Create customized index view class that handles login & registration
class MyAdminIndexView(AdminIndexView):
    @expose('/')
    @login_required
    def index(self):
        u = current_user()
        if not u.is_admin():
            abort(401)
        return super(MyAdminIndexView, self).index()


admin = Admin(name='论坛后台', index_view=MyAdminIndexView(), template_mode='bootstrap3')

admin.add_view(UserModelView(User, db.session, name='用户', endpoint='用户'))
admin.add_view(TopicModelView(Topic, db.session, name='主题', endpoint='主题'))
admin.add_view(BaseModelView(Reply, db.session, name='评论', endpoint='评论'))
admin.add_view(BoardModelView(Board, db.session, name='板块', endpoint='板块'))
