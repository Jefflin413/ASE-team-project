"""unit test for utils.db"""
from unittest import TestCase
import unittest
import utils.db

from flask import Flask
unittest.TestLoader.sortTestMethodsUsing = None


class TestDb(TestCase):
    # def setUp(self):
    #     print("setUp")
    def test_init_app(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.init_app(app)

    def test_init_db(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DROP TABLE user")
            utils.db.init_db()
            # self.assertEqual(True, "db" in g)
    # def test_init_db_command(self):
    #     app = Flask(__name__)
    #     with app.app_context():
    #         conn = utils.db.get_db()
    #         conn.execute("DROP TABLE user")
    #         utils.db.init_db_command()

    def test_close_db(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.get_db()
            utils.db.close_db()
    # def tearDown(self):
    #     print("tearDown")

