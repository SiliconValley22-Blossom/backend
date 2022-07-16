from sqlalchemy.sql.operators import exists

from myapp import db
from myapp.entity import User

class UserService:
    def save(self, userRequest):
       # self.isExist(userRequest.email)
        user = User(email=userRequest.email,
                    password=userRequest.password,
                    nickname=userRequest.nickname)
        db.session.add(user)
        db.session.commit()
        return user

   # def isExist(self, email):
      #  result = User.query.filter_by(email=email).count()
      #  print(result is None)

    def delete(self, userRequest):
        user = User(email=userRequest.email,
                    password=userRequest.password,
                    nickname=userRequest.nickname,
                    is_deleted=1)

        db.session.add(user)
        db.session.commit()
        return user