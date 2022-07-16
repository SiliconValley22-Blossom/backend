from myapp import db
from myapp.entity import User

class UserService:
    def save(self, userRequest):
        user = User(email=userRequest.email,
                    password=userRequest.password,
                    nickname=userRequest.nickname,
                    check_deleted=0)

        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, userRequest):
        user = User(email=userRequest.email,
                    password=userRequest.password,
                    nickname=userRequest.nickname,
                    check__deleted=1)

        db.session.add(user)
        db.session.commit()
        return user