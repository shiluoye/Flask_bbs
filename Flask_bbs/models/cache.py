import json

import redis

from models.topic import Topic


def cache_init():
    # 推荐使用StrictRedis,尽量不要使用redis.Redis
    cache = redis.StrictRedis()
    cache.flushdb()  # 清除当前数据库所有的key
    return cache


cache = cache_init()


def dict_to_object(form):
    topic = Topic()
    for name, value in form.items():
        setattr(topic, name, value)
    return topic


"""
在redis中的存储方式为：key(user_id)->value(这个人创建的所用话题（被转成字符串）)
"""


def created_topic(user_id):
    k = 'created_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        ts = [dict_to_object(t) for t in ts]
        return ts
    else:
        ts = Topic.created_topic(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


def replied_topic(user_id):
    k = 'replied_topic_{}'.format(user_id)
    if cache.exists(k):
        v = cache.get(k)
        ts = json.loads(v)
        ts = [dict_to_object(t) for t in ts]
        return ts
    else:
        ts = Topic.replied_topic(user_id=user_id)
        v = json.dumps([t.json() for t in ts])
        cache.set(k, v)
        return ts


def update_created_topic_cache(user_id):
    k = 'created_topic_{}'.format(user_id)

    ts = Topic.created_topic(user_id=user_id)
    v = json.dumps([t.json() for t in ts])
    cache.set(k, v)


def update_replied_topic_cache(user_id):
    k = 'replied_topic_{}'.format(user_id)

    ts = Topic.replied_topic(user_id=user_id)
    v = json.dumps([t.json() for t in ts])
    cache.set(k, v)
