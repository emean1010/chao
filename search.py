from app import configured_app
from model import User, School, College, Certify
from sqlalchemy import or_


def find(username=None, school_name=None, college_name=None):
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
    ).all()
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
    data = list(data_dict.values())
    for d in data:
        print(d)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        filters = dict(
            school_name='长沙',
            college_name='计算机',
        )
        find(**filters)