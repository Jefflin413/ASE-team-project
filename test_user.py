"""unit test for utils.user"""
from unittest import TestCase
import unittest
import utils.db

from flask import Flask

from utils.user import User
unittest.TestLoader.sortTestMethodsUsing = None

import os


class TestUser(TestCase):
    def setUp(self):
        os.system("git restore utils/sqlite_db")
        print("setUp")

    def test_create(self):
        app = Flask(__name__)
        with app.app_context():
            # print("test create")
            cur = utils.db.get_db()
            cur.execute("DELETE FROM user")
            id_ = "sw3525"
            name = "Carbon"
            email = "carbonhaha@gmail.com"
            profile_pic = "123.png"
            usertype = "Personal"
            User.create(id_, name, email, profile_pic, usertype)
            user = cur.execute("SELECT * FROM `user`")
            rows = user.fetchall()
            self.assertEqual(1, len(rows))
            self.assertEqual("sw3525", rows[0]['id'])
            self.assertEqual("Carbon", rows[0]['name'])
            self.assertEqual("carbonhaha@gmail.com", rows[0]['email'])
            self.assertEqual("123.png", rows[0]['profile_pic'])
            self.assertEqual("Personal", rows[0]['usertype'])

    def test_create_miss(self):
        app = Flask(__name__)
        with app.app_context():
            # print("test create")
            cur = utils.db.get_db()
            cur.execute("DELETE FROM user")
            id_ = "kkking"
            name = None
            email = "carbonhaha.com"
            profile_pic = "123.png"
            usertype = "Personal"
            User.create(id_, name, email, profile_pic, usertype)
            user = cur.execute("SELECT * FROM user where `id` = 'kkking'")
            rows = user.fetchall()
            # print(rows)
            self.assertEqual([], rows)

    def test_get(self):
        app = Flask(__name__)
        with app.app_context():
            id_ = "sw3525"
            name = "Carbon"
            email = "carbonhaha@gmail.com"
            profile_pic = "123.png"
            usertype = "Personal"
            User.create(id_, name, email, profile_pic, usertype)
            user = User.get("sw3525")
            self.assertEqual("sw3525", user.id)
            self.assertEqual("Carbon", user.name)
            self.assertEqual("carbonhaha@gmail.com", user.email)
            self.assertEqual("123.png", user.profile_pic)
            self.assertEqual("Personal", user.usertype)

            # print("Ahoy!")

    def test_get_miss(self):
        app = Flask(__name__)
        with app.app_context():
            id_ = "sw3525"
            name = "Carbon"
            email = "carbonhaha@gmail.com"
            profile_pic = "123.png"
            usertype = "Personal"
            User.create(id_, name, email, profile_pic, usertype)
            user = User.get("sw9999")
            self.assertEqual(None, user)
            # print("Ahoy!")

    def tearDown(self):
        os.system("git restore utils/sqlite_db")
        print("tearDown")
