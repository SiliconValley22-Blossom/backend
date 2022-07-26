import hashlib

from sqlalchemy import select
from werkzeug.exceptions import BadRequest, NotFound

from myapp import db
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