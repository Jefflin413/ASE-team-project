"""the user class"""

from .db import get_db


def get_streaming():
    """get the data of specific user"""
    db = get_db()
    res = db.execute(
        "SELECT * FROM streaming"
    ).fetchall()
    if not res:
        return None

    return res


def create_stream(id_, name, email, profile_pic, usertype):
    """create an user"""
    db = get_db()
    db.execute(
        "INSERT INTO user (id, name, email, profile_pic, usertype)"
        " VALUES (?, ?, ?, ?, ?)",
        (id_, name, email, profile_pic, usertype),
    )
    db.commit()
