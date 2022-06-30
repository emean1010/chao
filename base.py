from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer


__all__ = 'SQLMixin', 'db'


db = SQLAlchemy()


class SQLMixin(object):
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)

    @classmethod
    def new(cls, data):
        m = cls()
        for name, value in data.items():
            if hasattr(m, name):
                setattr(m, name, value)

        db.session.add(m)
        return m

    def update(self, **kwargs):
        for name, value in kwargs.items():
            setattr(self, name, value)

        db.session.add(self)

    @classmethod
    def one(cls, **kwargs):
        ms = cls.query.filter_by(**kwargs).first()
        return ms

    def info(self):
        data = dict()
        no_list = ['username', 'source', 'student_id', 'signature', 'is_auth', 'is_lock']
        for k, v in self.__dict__.items():
            if not k.startswith('_') and k not in no_list and v:
                data[k] = v
        return data
