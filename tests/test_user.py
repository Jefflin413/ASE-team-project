import sqlite3
from sqlite3 import Error
from unittest import TestCase
import unittest
import utils.db

from flask import Flask, g
from flask_login import LoginManager

from utils.user import User
unittest.TestLoader.sortTestMethodsUsing = None

class TestUser(TestCase):
    def setUp(self):
        print("setUp")
    def test_create(self):
        app = Flask(__name__)
        with app.app_context():
            print("test create")
            #self.fail("some message")
            # print(app.app_context().g.db)
            # conn = app.app_context().g['db']
            # db = g.pop('db', None)
            cur = utils.db.get_db()
            # try:
            # conn = sqlite3.connect("/Users/hym/PycharmProjects/ASE-team-project/utils/sqlite_db")
            # except Error as e:
            #     print(e)

            # cur = conn.cursor()
            cur.execute("DELETE FROM user")
            id_ = "sw3525"
            name = "Carbon"
            email = "carbonhaha@gmail.com"
            profile_pic = "123.png"
            usertype = "viewer"
            User.create(id_, name, email, profile_pic, usertype)
            user = cur.execute("SELECT * FROM user")
            rows = user.fetchall()
            self.assertEqual(1, len(rows))
            self.assertEqual("sw3525", rows[0]['id'])
            self.assertEqual("Carbon", rows[0]['name'])
            self.assertEqual("carbonhaha@gmail.com", rows[0]['email'])
            self.assertEqual("123.png", rows[0]['profile_pic'])
            self.assertEqual("viewer", rows[0]['usertype'])

            print("HIHI")

    def test_get(self):
        app = Flask(__name__)
        with app.app_context():
            print("test get")
            user = User.get("sw3525")
            self.assertEqual("sw3525", user.id)
            self.assertEqual("Carbon", user.name)
            self.assertEqual("carbonhaha@gmail.com", user.email)
            self.assertEqual("123.png", user.profile_pic)
            self.assertEqual("viewer", user.usertype)

            print("Ahoy!")

    def test_get_wrong_user(self):
        app = Flask(__name__)
        with app.app_context():
            print("test get")
            user = User.get("yh3328")
            self.assertEqual(None, user)

            print("Ahoy!")

    def tearDown(self):
        print("tearDown")
