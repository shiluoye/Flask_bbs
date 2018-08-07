import time

from pymongo import MongoClient

mongua = MongoClient()  # 默认host='localhost,port=27101


def next_id(name):
    query = {
        'name': name,
    }
    update = {
        '$inc': {
            'seq': 1
        }
    }

    kwargs = {
        'query': query,
        'update': update,
        'upsert': True,
        'new': True,
    }
    doc = mongua.db['data_id']
    new_id = doc.find_and_modify(**kwargs).get('seq')
    return new_id


def timestamp():
    return int(time.time())


class Mongua(object):
    __fields__ = [
        '_id',
        ('id', int, -1),
        ('type', str, ''),
        ('deleted', bool, False),
        ('created_time', int, 0),
        ('updated_time', int, 0),
    ]

    def save(self):
        name = self.__class__.__name__
        mongua.db[name].save(self.__dict__)

    @classmethod
    def new(cls, form=None, **kwargs):
        """
        new是给外部使用的函数，根据表单生成对象
        :param form:
        :param kwargs:
        :return:
        """
        name = cls.__name__
        # 创建一个空对象
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')
        if form is None:
            form = {}

        for f in fields:
            k, t, v = f
            if k in form:
                setattr(m, k, t(form[k]))
            else:
                setattr(m, k, v)

        for k, v in kwargs.items():
            if hasattr(m, k):
                setattr(m, k, v)
            else:
                raise KeyError
        m.id = next_id(name)
        ts = int(time.time())
        m.created_time = ts
        m.updated_time = ts
        m.type = name.lower()
        m.save()
        return m

    @classmethod
    def _new_with_bson(cls, bson):
        "从mongo数据中恢复一个model"
        m = cls()
        fields = cls.__fields__.copy()
        fields.remove('_id')  # 去除_id这个特殊的字段
        for f in fields:
            k, t, v = f
            if k in bson:
                setattr(m, k, bson[k])
            else:
                # 设置默认值
                setattr(m, k, v)
        setattr(m, '_id', bson['_id'])
        # 因为现在数据库中未必有type,所以这里强行加上
        m.type = cls.__name__.lower()
        return m

    @classmethod
    def _find(cls, **kwargs):
        """
        mongo数据查询
        :param kwargs:
        :return:
        """
        name = cls.__name__
        flag_sort = '__sort'
        sort = kwargs.pop(flag_sort, None)
        ds = mongua.db[name].find(kwargs)
        if sort is not None:
            ds = ds.sort(sort)
        l = [cls._new_with_bson(d) for d in ds]
        return l

    @classmethod
    def find_one(cls, **kwargs):
        l = cls._find(**kwargs)
        if len(l) > 0:
            return l[0]
        else:
            return None

    @classmethod
    def upsert(cls, query_form, update_form, hard=False):
        ms = cls.find_one(**query_form)
        # 如果没有查询到相应属性
        if ms is None:
            query_form.upadte(update_form)  # 合并两个字典
            ms = cls.new(query_form)
        else:
            ms.update(update_form, hard=hard)
        return ms

    def update(self, form, hard=False):
        for k, v in form.items():
            if hard or hasattr(self, k):
                setattr(self, k, v)
        self.save()
