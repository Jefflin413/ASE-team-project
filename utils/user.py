"""the user class"""
from flask_login import UserMixin

from .db import get_db


class User(UserMixin):
    """the user class"""
    def __init__(self, id_, name, email, profile_pic, usertype):
        self.id = id_
        self.name = name
        self.email = email
        self.profile_pic = profile_pic
        self.usertype = usertype

    @staticmethod
    def get(user_id):
        """get the data of specific user"""
        db = get_db()
        user = db.execute(
            "SELECT * FROM user WHERE id = ?", (user_id,)
        ).fetchone()
        if not user:
            return None

        user = User(
            id_=user[0], name=user[1], email=user[2], profile_pic=user[3], usertype=user[4]
        )
        return user

    @staticmethod
    def create(id_, name, email, profile_pic, usertype):
        """create an user"""
        if name is not None:
            db = get_db()
            db.execute(
                "INSERT INTO user (id, name, email, profile_pic, usertype)"
                " VALUES (?, ?, ?, ?, ?)",
                (id_, name, email, profile_pic, usertype),
            )
            db.commit()
        else:
            pass
