import json
from models.user import User
from models.mongua import Mongua,next_id
import logging
import os
import time

#处理markdown
from markdown import markdown
import bleach

from utils import log
ogger = logging.getLogger("bbs")

def process_text(text):
    html_text = markdown(text, output_format='html')

    # 允许的标签
    allow_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul', 'h1',
                  'h2', 'h3', 'p']
    # 允许的属性
    # 这样设置将不会过滤所有标签的class属性,和a标签的href,rel属性....
    attrs = {
        '*': ['class'],
        'a': ['href', 'rel'],
        'img': ['src', 'alt'],
    }

    cleaned_text = bleach.clean(html_text,
                                tags=allow_tags,
                                strip=True,
                                attributes=attrs
                                )
    return cleaned_text


def process_text2(text):
    text = markdown(text,extensions=[
                                      'markdown.extensions.extra',
                                      'markdown.extensions.codehilite',
                                      'markdown.extensions.toc',
                                  ])
    return text

class Cache(object):
    def get(self, key):
        pass

    def set(self, key, value):
        pass


class MemoryCache(Cache):
    def __init__(self):
        self.cache = {}

    def get(self, key):
        return self.cache[key]

    def set(self, key, value):
        self.cache[key] = value


class RedisCache(Cache):
    import redis
    redis_db = redis.StrictRedis(host='localhost', port=6379, db=0)

    def set(self, key, value):
        return RedisCache.redis_db.set(key, value)

    def get(self, key):
        return RedisCache.redis_db.get(key)


class Topic(Mongua):
    __fields__ = Mongua.__fields__ + [
        ('content', str, ''),
        ('title', str, -1),
        ('user_id', int, -1),
        ('board_id', int, -1),
        ('views', int, 0)
    ]

    @classmethod
    def new(cls, form=None, **kwargs):
        name = cls.__name__
        # 创建一个空对象
        m = cls()
        # 把定义的数据写入空对象, 未定义的数据输出错误
        fields = cls.__fields__.copy()
        # 去掉 _id 这个特殊的字段
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                # 设置默认值
                setattr(m, k, v)
        # 处理额外的参数 kwargs
        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        # 写入默认数据
        m.id = next_id(name)
        # print('debug new id ', m.id)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        # m.deleted = False
        m.type = name.lower()
        m.content=process_text2(m.content)
        m.save()
        return m

    should_update_all = True
    # 1. memory cache
    cache = MemoryCache()
    # 2. redis cahce
    redis_cache = RedisCache()
    def to_json(self):
        d = dict()
        for k in Topic.__fields__:
            key = k[0]
            if not key.startswith('_'):
                d[key] = getattr(self,key)
        return json.dumps(d)

    @classmethod
    def from_json(cls, j):
        d = json.loads(j)

        instance = cls()
        for k, v in d.items():
            setattr(instance, k, v)
        return instance

    @classmethod
    def all_delay(cls):
        time.sleep(3)
        return Topic.all()

    @classmethod
    def get(cls, id):
        m = cls.find_by(id=id)
        m.views += 1
        m.save()
        return m

    def save(self):
        super(Topic, self).save()
        should_update_all = True

    @classmethod
    def cache_all(cls):

        #2. redis cache
        if Topic.should_update_all:
            Topic.redis_cache.set('topic_all', json.dumps([i.to_json() for i in cls.all_delay()]))
            Topic.should_update_all = False
        j = json.loads(Topic.redis_cache.get('topic_all').decode('utf-8'))
        j = [Topic.from_json(i) for i in j]
        return j



    def replies(self):
        from .reply import Reply
        ms = Reply.find_all(topic_id=self.id)
        return ms

    def board(self):
        from .board import Board
        m = Board.find(self.board_id)
        return m

    def user(self):
        u = User.find(id=self.user_id)
        return u
