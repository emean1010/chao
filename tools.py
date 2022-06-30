import csv

from app import configured_app
from base import db
from model import User, Certify, School, College


def log(*args, **kwargs):
    with open('running.log.txt', 'a', encoding='utf-8') as f:
        print(*args, file=f, **kwargs)
        print(*args, **kwargs)


class MyClass(object):
    def __init__(self):
        self.stop = False
        self.times = 0
        self.lost = set()

        self.index = 0
        self.token = ''
        self.tokens = []
        self.keys = []
        self.values = []
        self.is_key = True
        self.certify_start = 0
        self.certify_keys = ['college_name', 'role', 'code', 'position_id', 'enrollment_year', 'school_id',
                             'college_id', 'major_name', 'type', 'school_name', 'user_id', 'certify_id']

    def reset(self):
        self.index = 0
        self.token = ''
        self.tokens = []
        self.keys = []
        self.values = []
        self.is_key = True

    def clean_key(self):
        filter_char = ['_', '"', '{', '[']
        n = ''
        for i in self.token:
            if i not in filter_char:
                n += i
        return n

    def clean_value(self):
        filter_char = ['"', '{', '[', ']', '}']
        n = ''
        for i in self.token:
            if i not in filter_char:
                n += i
        return n

    def add_token(self, ):
        filter_keys = ['_source', 'certifyDocList', 'stuCourseDocList']
        if self.token in filter_keys:
            if self.certify_start == 0 and self.token == 'certifyDocList':
                self.certify_start = len(self.keys)
            self.token = ''
            return

        if self.is_key:
            if self.token.find('null') < 0:
                t = self.clean_key()
                self.keys.append(t)
        else:
            t = self.clean_value()
            self.values.append(t)
        self.is_key = not self.is_key
        self.token = ''

    def read_token(self, s):
        index = 0
        while index < len(s):
            i = s[index]
            if i == ':':
                # key 读取结束
                if s[index-2:index] not in ['ps', 'tp'] and ord(s[index-1]) < 30000:
                    self.add_token()
                else:
                    self.token += i
            elif i == ',':
                last = s.find(':', index)
                stop = s.find(',', index+1)
                # value 读取结束
                if stop > last or stop < 0:
                    self.add_token()
                else:
                    self.token += i
            else:
                self.token += i
            index += 1
        if self.token:
            self.lost.add(self.token)

    def read_csv(self):
        user_len = User.query.count()
        f = open(r'chi.csv', 'r', encoding='utf-8', newline='\n')
        with f:
            reader = csv.reader(f)
            for row in reader:
                row_str = ','.join(row)
                self.times += 1
                e = user_len - 1000
                if self.times < e:
                    continue
                # elif self.times > e:
                #     break
                # print(row_str)
                print(self.times)
                self.reset()
                self.read_token(row_str)
                # print(row_str)
                if len(self.keys) != len(self.values):
                    log(row_str)
                self.save()
                if self.stop:
                    break

    def save(self):
        data = dict()
        certify_list = []
        for index, i in enumerate(self.keys):
            v = self.values[index]
            if v == 'null':
                continue
            k = ''
            for j in i:
                if j.isupper():
                    k += '_'
                    k += j.lower()
                else:
                    k += j
            if k.startswith('_'):
                k = k[1:]
            if k in ['college_id', 'school_id']:
                v = int(v)
            # 保存主表字段
            if index < self.certify_start or k not in self.certify_keys:
                data[k] = v
            # 保存 certify 表 字段
            else:
                write_in = False
                while not write_in:
                    for cd in certify_list:
                        if k not in cd:
                            cd[k] = v
                            write_in = True
                    if not write_in:
                        new_dict = dict()
                        certify_list.append(new_dict)

        user = User.one(student_id=data['id'])
        if user:
            return

        user = User.new(data)
        db.session.flush()
        # print('save user over')
        for c in certify_list:
            c.update(user_id=user.id)
            mc = Certify.new(c)
            # print('save-------')
            School.save(c)
            College.save(c)

        db.session.commit()


if __name__ == '__main__':
    app = configured_app()
    with app.app_context():
        mc = MyClass()
        mc.read_csv()
        print('lost', mc.times, mc.lost)
