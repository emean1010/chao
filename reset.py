from sqlalchemy import create_engine

from app import configured_app
from base import db
from secret import database_password


def reset_database():
    url = f'mysql+pymysql://root:{database_password}@localhost/?charset=utf8mb4'
    e = create_engine(url, echo=True)

    with e.connect() as c:
        c.execute('DROP DATABASE IF EXISTS chao')
        c.execute('CREATE DATABASE IF NOT EXISTS chao CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci')
        c.execute('USE chao')

    db.metadata.create_all(bind=e)


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        reset_database()
