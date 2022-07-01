import os

from flask import render_template, request, Blueprint, send_file

from model import *
from operate import Operate

main = Blueprint('index', __name__)


def get_request_form():
    """获取 request 对象中的 输入参数 """
    if request.method == 'GET':
        form = request.args.to_dict()
    elif request.json:
        form = request.json
    else:
        form = request.form.to_dict()
    data = dict()
    for k, v in form.items():
        if v:
            data[k] = v

    return data


@main.route("/", methods=['GET', 'POST'])
def index():
    form = get_request_form()
    school_name = form.get('school_name', '')
    college_name = form.get('college_name', '')
    page = int(form.get('page', 1))
    limit = int(form.get('limit', 20))
    offset = (page - 1) * limit
    form.update(
        school_name=school_name,
        college_name=college_name,
        limit=limit,
        offset=offset,
        page=page,
    )
    print('index form', form)
    data = Operate.find(form)
    return render_template("index.html", data=data, **form)


@main.route("/images/<user_id>")
def image_get(user_id):
    file_path = os.path.join(os.curdir, 'default.png')
    u = User.one(id=user_id)
    if u and u.image:
        img_path = os.path.join(os.curdir, 'images', u.image)
        if os.path.isdir(img_path):
            file_path = img_path
    return send_file(file_path)


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
