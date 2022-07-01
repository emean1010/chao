from app import configured_app
from operate import Operate


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        filters = dict(
            school_name='长沙',
            college_name='计算机',
        )
        data = Operate.find(filters)
        for d in data:
            print(d)
