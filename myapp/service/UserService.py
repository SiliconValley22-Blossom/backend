import string
import random
from datetime import datetime
from threading import Thread

from flask import jsonify, current_app
from flask_mail import Message
from sqlalchemy import select, and_
from werkzeug.exceptions import BadRequest, NotFound, Unauthorized

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

    def isExistByEmail(self, email) -> bool:
        result = User.query.filter_by(email=email).count()
        return True if result else False

    def deleteById(self, user_id):
        result = User.query.filter_by(user_id=user_id).first()
        if result is None or result.is_deleted == 1:
            raise NotFound(description="존재하지 않습니다")
        result.is_deleted = 1
        db.session.commit()

    def modifyPassword(self, curUser, data):
        target = User.query.filter(User.email == curUser).first()
        pw_hash = encrypt(data.get('password'))

        if target.password != pw_hash:
            raise Unauthorized(www_authenticate="/api/login", description="비밀번호가 일치하지 않습니다.")
        if pw_hash == target.password:
            new_pw_hash = encrypt(data.get('new_password'))
            target.password = new_pw_hash
            target.updated_at = datetime.utcnow()

            db.session.add(target)
            db.session.commit()
            resp = jsonify({'message': '비밀번호가 변경되었습니다.'})
            return resp

    def sendPassword(self, curUser):
        target = User.query.filter(User.email == curUser).first()
        tmp_pw = createTempPassword()
        tmp_pw_hash = encrypt(tmp_pw)
        target.password = tmp_pw_hash
        target.updated_at = datetime.utcnow()

        db.session.add(target)
        db.session.commit()

        content = '{nick}님의 임시 비밀번호는 [{pw}]입니다.'.format(nick=target.nickname, pw=tmp_pw)
        send_email(content,"seonvelop@gmail.com")
        resp = jsonify({'message': '회원님의 이메일로 비밀번호를 전송하였습니다.'})
        return resp

    def getUserInfo(self, curUser):
        target = User.query.filter(and_(User.email==curUser)).first()
        resp=jsonify({
            'user_id':target.user_id,
            'email':target.email,
            'nickname':target.nickname,
            'updated_at':target.updated_at
        })
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
    app = current_app._get_current_object()
    msg = Message("[BLOSSOM] 임시 비밀번호 발급 안내",sender="seonvelop@gmail.com", recipients=[to])
    msg.body = content
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr