from sqlalchemy import and_
from werkzeug.exceptions import Forbidden

from myapp import db
from myapp.entity import User


class AdminService:
    def __init__(self, email):
        target = User.query.filter(and_(User.email == email, User.user_role == 'admin')).first()
        if target:
            return
        else:
            raise Forbidden(description="접근이 제한되었습니다.")

    def deleteUserForcefully(self, idList):
        targets = User.query.filter(User.user_id.in_(idList)).all()
        for tar in targets:
            tar.is_deleted = True
            for photo in tar.photo:
                photo.is_deleted = True
            db.session.add(tar)
        db.session.commit()

    def getAllUsers(self, page):
        userList = User.query \
            .filter(User.is_deleted==False)\
            .order_by(User.created_at)\
            .all()

        # 1페이지 당 30명 씩 보기 => page*30 + 30
        # result = user_list.paginate(page, per_page=3).items
        return userList