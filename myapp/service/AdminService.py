from myapp import db
from myapp.entity import User


class AdminService:
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
            .order_by(User.created_at)\
            .all()

        # 1페이지 당 30명 씩 보기 => page*30 + 30
        # result = user_list.paginate(page, per_page=3).items
        return userList