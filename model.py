from sqlalchemy import Column, String, Integer

from base import db, SQLMixin


class User(SQLMixin, db.Model):
    """ 用户表 """
    student_id = Column(String(20))
    score = Column(Integer)
    username = Column(String(50))
    realname = Column(String(50))
    email = Column(String(50))
    area = Column(Integer)
    mobile = Column(String(20))
    avatar = Column(String(200))
    gender = Column(Integer)
    is_auth = Column(Integer)
    source = Column(String(20))
    is_lock = Column(Integer)
    signature = Column(String(20))
    qq = Column(String(20))
    ym = Column(String(10))

    @classmethod
    def new(cls, data):
        data.update(student_id=data['id'])
        data.pop('id')
        if 'email' in data:
            email = data['email']
            index = email.find('\\r')
            if index > 0:
                email = email[:index]
            if email.endswith('.ddd'):
                email = email[:len(email)-4] + '.com'
            data['email'] = email
        if 'mobile' in data:
            mobile = data['mobile']
            if mobile[0] == '0':
                data['mobile'] = '1' + mobile[1:]
        if 'avatar' in data:
            data['ym'] = data['avatar'].split('/')[-2]
        m = super().new(data)
        return m


class School(SQLMixin, db.Model):
    name = Column(String(50))

    @classmethod
    def save(cls, data):
        if 'school_id' in data:
            school_id = data['school_id']
            school = cls.one(id=school_id)
            if not school and 'school_name' in data:
                form = dict(
                    id=school_id,
                    name=data['school_name']
                )
                school = cls.new(form)


class College(SQLMixin, db.Model):
    school_id = Column(Integer)
    name = Column(String(50))

    @classmethod
    def save(cls, data):
        if 'college_id' in data:
            college_id = data['college_id']
            college = cls.one(id=college_id)
            if not college and 'college_name' in data:
                form = dict(
                    id=college_id,
                    school_id=data['school_id'],
                    name=data['college_name']
                )
                college = cls.new(form)


class Certify(SQLMixin, db.Model):
    """ 用户表 """
    user_id = Column(Integer)
    certify_id = Column(String(20))
    school_id = Column(Integer)
    type = Column(Integer)
    role = Column(Integer)
    code = Column(String(20))
    college_id = Column(Integer)
    position_id = Column(Integer)
    enrollment_year = Column(String(20))
    major_name = Column(String(50))
