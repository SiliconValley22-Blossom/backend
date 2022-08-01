import random
import string
from datetime import datetime
from threading import Thread

from flask import jsonify, current_app
from flask_mail import Message
from sqlalchemy import and_
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
            hashedPassword = encrypt(userRequest.password)
            user = User(email=userRequest.email,
                        password=hashedPassword,
                        nickname=userRequest.nickname)
            db.session.add(user)
            db.session.commit()
            return user

    def isExistByEmail(self, email):
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
        hashedPassword = encrypt(data.get('password'))

        if target.password != hashedPassword:
            raise Unauthorized(www_authenticate="/api/users", description="비밀번호가 일치하지 않습니다.")
        if hashedPassword == target.password:
            newHashedPassword = encrypt(data.get('new_password'))
            target.password = newHashedPassword
            target.updated_at = datetime.utcnow()

            db.session.commit()
            resp = jsonify({'message': '비밀번호가 변경되었습니다.'})
            return resp

    def sendPassword(self, email):
        target = User.query.filter(User.email == email).first()
        if target is None:
            raise Unauthorized(www_authenticate="/api/users/reset-password", description=f"{email}에 해당하는 회원 정보가 없습니다.")
        tempPassword = createTempPassword()
        hashedTempPassword = encrypt(tempPassword)
        target.password = hashedTempPassword
        target.updated_at = datetime.utcnow()

        db.session.commit()

        content = f'{target.nickname}님의 임시 비밀번호는 [{tempPassword}]입니다.'
        sendEmail(content, "seonvelop@gmail.com")
        resp = jsonify({'message': '회원님의 이메일로 비밀번호를 전송하였습니다.'})
        return resp

    def getUserInfo(self, curUser):
        target = User.query.filter(and_(User.email == curUser)).first()
        resp = jsonify({
            'user_id': target.user_id,
            'email': target.email,
            'nickname': target.nickname,
            'created_at': target.created_at,
            'updated_at': target.updated_at,
            'is_deleted': target.is_deleted
        })
        return resp


def createTempPassword():
    '''길이가 10인 영어 대소문자 + 숫자 무작위 조합 문자열 생성'''
    tempPasswordLength = 10
    candidate = string.ascii_letters + string.digits

    tempPassword = ""
    for i in range(tempPasswordLength):
        tempPassword += random.choice(candidate)
    return tempPassword


def sendAsyncEmail(app, msg):
    with app.app_context():
        mail.send(msg)


def sendEmail(content, to):
    app = current_app._get_current_object()
    msg = Message("[BLOSSOM] 임시 비밀번호 발급 안내", sender="seonvelop@gmail.com", recipients=[to])
    msg.body = content
    thr = Thread(target=sendAsyncEmail, args=[app, msg])
    thr.start()
    return thr