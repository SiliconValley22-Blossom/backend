from sqlalchemy.sql.operators import exists

from myapp import db
from myapp.entity import User

class UserService:
    def save(self, userRequest):
        if(self.isExist(userRequest.email)):
            raise Exception("이미 존재하는 회원입니다")
        user = User(email=userRequest.email,
                    password=userRequest.password,
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