from model import User, School, College, Certify


class Operate(object):

    @staticmethod
    def find(username=None, school_name=None, college_name=None, limit=20, offset=0):
        q = User.query\
            .outerjoin(Certify, Certify.user_id == User.id)\
            .outerjoin(School, School.id == Certify.school_id)\
            .outerjoin(College, College.school_id == School.id)

        # q = q.filter(or_(User.gender == 1, User.gender.is_(None)))
        if username:
            q = q.filter(User.username.like(f'%{username}%'))
        if school_name:
            q = q.filter(School.name.like(f'%{school_name}%'))
        if college_name:
            q = q.filter(College.name.like(f'%{college_name}%'))

        ms = q.add_columns(
            School.name.label('school_name'),
            College.name.label('college_name'),
        ).limit(limit).offset(offset).all()
        data_dict = dict()
        for m in ms:
            user = m[0]
            user_id = user.id
            if user_id not in data_dict:
                user_info = user.info()
                school_info = []
            else:
                user_info = data_dict[user_id]
                school_info = user_info['school_info']

            school_cell = [m[1], m[2]]
            school_info.append(school_cell)

            user_info.update(school_info=school_info)
            data_dict[user_id] = user_info
        rows = list(data_dict.values())
        return rows
