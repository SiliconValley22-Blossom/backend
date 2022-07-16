import hashlib

from werkzeug.exceptions import BadRequest

from myapp import db
from myapp.entity import User
from myapp.util import encrypt


class UserService:
    def save(self, userRequest):
        # 중복 회원가입 방지
        if self.isExist(userRequest.email):
            raise BadRequest(description="이미 존재하는 회원입니다")
        # 새로운 회원
        else:
            pw_hash = encrypt(userRequest.password)
            print(pw_hash)
        user = User(email=userRequest.email,
                    password=pw_hash,
                    nickname=userRequest.nickname)
        db.session.add(user)
        db.session.commit()
        return user

    def isExist(self, email):
        result = User.query.filter_by(email=email).count()
        print(result)
        return result >= 1

    def delete(self, userRequest):
        user = User(email=userRequest.email,
                    password=userRequest.password,
                    nickname=userRequest.nickname,
                    is_deleted=1)

        db.session.add(user)
        db.session.commit()
        return user