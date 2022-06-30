from flask import Flask

from base import db
from route import main as index_routes
from secret import database_password


def configured_app():
    _app = Flask(__name__)

    uri = f'mysql+pymysql://root:{database_password}@localhost/chao?charset=utf8mb4'
    _app.config['SQLALCHEMY_DATABASE_URI'] = uri
    _app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(_app)

    _app.register_blueprint(index_routes)

    return _app


app = configured_app()


if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.jinja_env.auto_reload = True
    config = dict(
        host='0.0.0.0',
        port=3000,
    )
    app.run(**config)
