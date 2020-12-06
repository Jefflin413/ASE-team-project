"""unit test for utils.db"""
import unittest
from unittest import TestCase

from flask import Flask

import utils.db
import os
from datetime import date, datetime

unittest.TestLoader.sortTestMethodsUsing = None


class TestDb(TestCase):

    def setUp(self):
        os.system("git restore utils/sqlite_db")
        print("setUp")

    def test_get_db(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            self.assertTrue(conn)

    def test_close_db(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn = utils.db.close_db()
            self.assertEqual(None, conn)

    def test_init_db(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DROP TABLE IF EXISTS `user`")
            conn.execute("DROP TABLE IF EXISTS  watch_history")
            conn.execute("DROP TABLE IF EXISTS  streaming")
            conn.execute("DROP TABLE IF EXISTS  audience_comment")
            conn.execute("DROP TABLE IF EXISTS  advertise")
            utils.db.init_db()
            res = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
            tables = ["user", "watch_history", "streaming", "audience_comment", "advertise"]
            for i, r in enumerate(res):
                # print(r['name'])
                self.assertEqual(tables[i], r['name'])

    ## NOT SURE 1
    # def test_init_db_command(self):
    #     app = Flask(__name__)
    #     with app.app_context():
    #         conn = utils.db.get_db()
    #         # conn.execute("DROP TABLE `user`")
    #         res = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
    #         for i, r in enumerate(res):
    #             print(r['name'])
    #         utils.db.init_db_command()

    ## NOT SURE 2
    # def test_init_app(self):
    #     app = Flask(__name__)
    #     with app.app_context():
    #         utils.db.init_app(app)
    #         conn = utils.db.get_db()
    #         res = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
    #         tables = ["user", "watch_history", "streaming", "audience_comment", "advertise"]
    #         for i, r in enumerate(res):
    #             # print(r['name'])
    #             self.assertEqual(tables[i], r['name'])


    def test_get_streaming(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            res = utils.db.get_streaming()
            self.assertTrue(res[0])

    def test_get_streaming_empty(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from streaming")
            res = utils.db.get_streaming()
            self.assertEqual(None, res)

    def test_create_stream(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            res = conn.execute("SELECT * FROM streaming").fetchall()
            # print(res[-1].keys())
            self.assertEqual("unit_test001", res[-1]['id'])
            self.assertEqual("unit_test1", res[-1]['name'])
            self.assertEqual("Life", res[-1]['category'])

    def test_update_stream(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.update_stream("unit_test001", "https://www.HIHI.m3u8")
            res = conn.execute("SELECT * FROM streaming").fetchall()
            # print(res[-1].keys())
            self.assertEqual("unit_test001", res[-1]['id'])
            self.assertEqual("https://www.HIHI.m3u8", res[-1]['m3u8_URL'])

    def test_update_stream_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.update_stream("unit_test999", "https://www.HIHI.m3u8")
            res = conn.execute("SELECT * FROM streaming where `id` = 'unit_test999'").fetchall()
            # print(res[-1].keys())
            self.assertEqual([], res)

    def test_get_streaming_m3u8(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.update_stream("unit_test001", "https://www.HIHI.m3u8")
            res = utils.db.get_streaming_m3u8("unit_test001")
            # print(res[-1].keys())
            self.assertTrue(res)

    def test_get_streaming_m3u8_none(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from streaming where `id` = 'unit_test999'")
            res = utils.db.get_streaming_m3u8("unit_test999")
            # print(res[-1].keys())
            self.assertEqual(None, res)

    def test_get_current_watching(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.update_stream("unit_test001", "https://www.HIHI.m3u8")
            utils.db.update_current_watching("unit_test001")
            res = utils.db.get_current_watching("unit_test001")
            self.assertEqual(1, res)

    def test_get_current_watching_none(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from streaming where `id` = 'unit_test999'")
            res = utils.db.get_current_watching("unit_test999")
            # print(res[-1].keys())
            self.assertEqual(None, res)

    def test_update_current_watching_increase(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.update_stream("unit_test001", "https://www.HIHI.m3u8")
            utils.db.update_current_watching("unit_test001")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * FROM streaming").fetchall()
            # print(res[-1].keys())
            self.assertEqual(1, res[-1]['current_watching'])

    def test_update_current_watching_increase_none(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from streaming where `id` = 'unit_test999'")
            res = utils.db.update_current_watching("unit_test999")
            # print(res[-1].keys())
            self.assertEqual(None, res)

    def test_update_current_watching_decrease(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.update_stream("unit_test001", "https://www.HIHI.m3u8")
            utils.db.update_current_watching("unit_test001", False)
            conn = utils.db.get_db()
            res = conn.execute("SELECT * FROM streaming").fetchall()
            # print(res[-1].keys())
            self.assertEqual(-1, res[-1]['current_watching'])

    def test_update_current_watching_decrease_none(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from streaming where `id` = 'unit_test999'")
            res = utils.db.update_current_watching("unit_test999", False)
            # print(res[-1].keys())
            self.assertEqual(None, res)

    def test_delete_stream(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.update_stream("unit_test001", "https://www.HIHI.m3u8")
            utils.db.delete_stream("unit_test001")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * from streaming where `id` = 'unit_test001'").fetchall()
            self.assertEqual(0, len(res))

    def test_delete_stream_miss(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.update_stream("unit_test001", "https://www.HIHI.m3u8")
            utils.db.delete_stream("unit_test111")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * from streaming where `id` = 'unit_test001'").fetchall()
            self.assertEqual(1, len(res))

    def test_insert_watch_history(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.create_stream("unit_test001", "unit_test1", "Life")
            utils.db.insert_watch_history("unit_test001", "unit_test1", "Life")
            res = conn.execute("SELECT * FROM streaming").fetchall()
            # print(res[-1].keys())
            self.assertEqual("unit_test001", res[-1]['id'])
            self.assertEqual("unit_test1", res[-1]['name'])
            self.assertEqual("Life", res[-1]['category'])

    def test_insert_watch_history_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.insert_watch_history("unit_test001", "unit_test1", "Life")
            res = conn.execute("SELECT * FROM streaming where `id`='unit_test111'").fetchall()
            # print(res[-1].keys())
            self.assertEqual(0, len(res))

    def test_update_watch_history(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
            utils.db.update_watch_history("b9073fb4-35e7-11eb-9844-0e6eb579fb2b")
            res = conn.execute("SELECT * FROM watch_history where UUID = 'b9073fb4-35e7-11eb-9844-0e6eb579fb2b'").fetchall()
            # print(res[-1].keys())
            self.assertEqual(time, res[-1]['end_time'])

    def test_update_watch_history_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.update_watch_history("UUIC999")
            res = conn.execute("SELECT * FROM watch_history where UUID = 'UUIC999'").fetchall()
            # print(res[-1].keys())
            self.assertEqual([], res)


    def tearDown(self):
        os.system("git restore utils/sqlite_db")
        print("tearDown")

