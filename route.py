from flask import render_template, request, Blueprint

from model import *

main = Blueprint('index', __name__)


def get_request_form():
    """获取 request 对象中的 输入参数 """
    if request.method == 'GET':
        form = request.args.to_dict()
    elif request.json:
        form = request.json
    else:
        form = request.form.to_dict()

    return form


@main.route("/")
def index():
    form = get_request_form()
    data = User.query.all()
    return render_template("index.html", data=data)


@main.route("/ss")
def school_get():
    ms = School.query.all()
    data = [m.info() for m in ms]
    res = dict(code=0, msg='ok', data=data)
    return res


@main.route("/cs/<school_id>")
def college_get(school_id):
    ms = College.query.filter(school_id=school_id).all()
    data = [m.info() for m in ms]
    res = dict(code=0, msg='ok', data=data)
    return res
