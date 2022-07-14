from myapp import db
from myapp.entity import User


class UserService:

    def save(self, userRequest):
        user = User(email=userRequest.email,
                    password=userRequest.password,
                    nickname=userRequest.nickname)

        db.session.add(user)
        db.session.commit()
        return user