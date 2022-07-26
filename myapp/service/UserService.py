import string
import random
from threading import Thread

from flask import jsonify, current_app
from flask_mail import Message
from sqlalchemy import select
from werkzeug.exceptions import BadRequest, NotFound

from myapp import db, mail
from myapp.entity import User
from myapp.util import encrypt


class UserService:
    def save(self, userRequest):
        # 중복 회원가입 방지
        if self.isExistByEmail(userRequest.email):
            raise BadRequest(description="이미 존재하는 회원입니다")
        # 새로운 회원
        else:
            pw_hash = encrypt(userRequest.password)
        user = User(email=userRequest.email,
                    password=pw_hash,
                    nickname=userRequest.nickname)
        db.session.add(user)
        db.session.commit()
        return user

    def isExistByEmail(self, email):
        result = User.query.filter_by(email=email).count()
        print(result)
        return result >= 1

    def deleteById(self, user_id):
        result = User.query.filter_by(user_id=user_id).first()
        if result is None or result.is_deleted == 1:
            raise NotFound(description="존재하지 않습니다")
        result.is_deleted = 1
        db.session.commit()

    def modifyPassword(self, curUser, data):
        target = User.query.filter(User.email == curUser).first()
        pw_hash = encrypt(data.get('password'))

        if pw_hash == target.password:
            new_pw_hash = encrypt(data.get('new_password'))
            target.password = new_pw_hash
            db.session.add(target)
            db.session.commit()
            resp = jsonify({'message': '비밀번호가 변경되었습니다.'})
        else:
            resp = jsonify({'message': '비밀번호가 맞지 않습니다.'})
            resp.status = 400
        return resp

    def sendPassword(self, curUser):
        target = User.query.filter(User.email == "qwe").first()
        tmp_pw = createTempPassword()
        tmp_pw_hash = encrypt(tmp_pw)
        target.password = tmp_pw_hash

        db.session.add(target)
        db.session.commit()

        content = '{nick}님의 임시 비밀번호는 [{pw}]입니다.'.format(nick=target.nickname, pw=tmp_pw)
        print(1)
        send_email(content,"seonvelop@gmail.com")
        print(4)
        resp = jsonify({'message': '회원님의 이메일로 비밀번호를 전송하였습니다.'})
        return resp


def createTempPassword():
    '''길이가 10인 영어 대소문자 + 숫자 무작위 조합 문자열 생성'''
    tmp_pw_len = 10
    pw_candidate = string.ascii_letters + string.digits

    tmp_pw = ""
    for i in range(tmp_pw_len):
        tmp_pw += random.choice(pw_candidate)
    return tmp_pw

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(content, to):
    print(2)
    app = current_app._get_current_object()
    msg = Message("[BLOSSOM] 임시 비밀번호 발급 안내 ",sender="seonvelop@gmail.com", recipients=[to])
    msg.body = content
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    print(3)
    return thr