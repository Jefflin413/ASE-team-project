"""unit test for utils.db and utils.user"""
import unittest
from unittest import TestCase

from flask import Flask
from flask import current_app, g
import utils.db
import utils.user
from utils.user import User
import os
from datetime import date, datetime

unittest.TestLoader.sortTestMethodsUsing = None


class TestDb(TestCase):

    # make sure any test never affect the application or other tests in db.
    def setUp(self):
        os.system("git restore utils/sqlite_db")
        print("setUp")

    def test_get_db(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            self.assertTrue(conn)

    def test_get_db_miss(self):
        os.system("rm utils/sqlite_db")
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            os.system("git restore utils/sqlite_db")
            self.assertTrue(conn)

    def test_close_db(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.get_db()
            utils.db.close_db()
            self.assertNotIn("db", g)

    def test_close_db_miss(self):
        os.system("rm utils/sqlite_db")
        app = Flask(__name__)
        with app.app_context():
            utils.db.close_db()
            self.assertNotIn("db", g)

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

    # # NOT SURE 1
    # def test_init_db_command(self):
    #     app = Flask(__name__)
    #     with app.app_context():
    #         conn = utils.db.get_db()
    #         # conn.execute("DROP TABLE `user`")
    #         res = conn.execute("SELECT * FROM sqlite_master WHERE type='table'").fetchall()
    #         for i, r in enumerate(res):
    #             print(r['name'])
    #         utils.db.init_db_command()


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

    def test_create_stream_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.create_stream("unit_test001", None, "Life")
            res = conn.execute("SELECT * FROM streaming where `id` = 'unit_test001'").fetchall()
            # print(res[-1].keys())
            self.assertEqual([], res)

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

    def test_get_streaming_m3u8_miss(self):
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

    def test_get_current_watching_miss(self):
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

    def test_update_current_watching_increase_miss(self):
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

    def test_update_current_watching_decrease_miss(self):
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
            utils.db.insert_watch_history("KIKI", "test1", "KIKI777")
            res = conn.execute("SELECT * FROM streaming").fetchall()
            # print(res[-1].keys())
            self.assertEqual("test3", res[-1]['id'])

    def test_insert_watch_history_streamer_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.insert_watch_history("unit_test001", None, "Life")
            res = conn.execute("SELECT * FROM streaming").fetchall()
            self.assertEqual("test3", res[-1]['id'])

    def test_insert_watch_history_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.insert_watch_history("unit_test001", "unit_test11", "Life")
            res = conn.execute("SELECT * FROM streaming where `id`='unit_test111'").fetchall()
            # print(res[-1].keys())
            self.assertEqual(0, len(res))

    def test_update_watch_history(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-10]
            utils.db.update_watch_history("b9073fb4-35e7-11eb-9844-0e6eb579fb2b")
            res = conn.execute("SELECT * FROM watch_history where UUID = 'b9073fb4-35e7-11eb-9844-0e6eb579fb2b'").fetchall()
            self.assertEqual(time, res[-1]['end_time'][:-7])

    def test_update_watch_history_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.update_watch_history("UUID999")
            res = conn.execute("SELECT * FROM watch_history where UUID = 'UUIC999'").fetchall()
            # print(res[-1].keys())
            self.assertEqual([], res)

    def test_get_watch_history(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_watch_history("test1")
            self.assertEqual("streamer id: test2, from 2020-11-30", res[0][:35])

    def test_get_watch_history_miss(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_watch_history("Alice")
            self.assertEqual(None, res)

    def test_get_watch_history_not_end(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_watch_history("101034240973870390330")
            # print(res[0])
            self.assertEqual("streamer id: test1, from 2020-12-04", res[0][:35])

    def test_get_analytics_category_all(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_analytics_category_all()
            # print(res[0], res[1])
            self.assertEqual(res[1][0], res[0][0]['x'])
            self.assertEqual(32, res[0][0]['value'])

    def test_get_analytics_category_all_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from watch_history")
            res = utils.db.get_analytics_category_all()
            self.assertEqual(None, res)

    def test_get_analytics_category(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_analytics_category("Life")
            # print(res)
            self.assertEqual('2020-11-20', res[0][0]['date'])

    def test_get_analytics_category_miss(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_analytics_category("New York")
            # print(res)
            self.assertEqual(None, res)

    def test_get_analytics_user_all(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_analytics_user_all()
            # print(res[0], res[1])
            self.assertEqual(res[1][0], res[0][0]['x'])
            self.assertEqual(32, res[0][0]['value'])

    def test_get_analytics_user_all_miss(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from watch_history")
            res = utils.db.get_analytics_user_all()
            # print(res[0], res[1])
            self.assertEqual(None, res)

    def test_get_analytics_user(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_analytics_user("test1")
            print(res[0], res[1])
            self.assertEqual('2020-11-20', res[0][0]['date'])
            self.assertEqual(2, res[0][0]['value'])
            self.assertEqual('test1', res[1][0])

    def test_get_analytics_user_miss(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_analytics_user("Patty")
            self.assertEqual(None, res)

    def test_update_user(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.update_user("test2", name="Claire", email="CYYoung.com", profile_pic="Y.jpg", usertype="Personal")
            res = conn.execute("SELECT * FROM `user` where `id` = 'test2'").fetchall()
            # print(res)
            self.assertEqual("Claire", res[-1]['name'])

    def test_update_user_miss_id(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            utils.db.update_user("CYYoung", name="Claire", email="CYYoung.com", profile_pic="Y.jpg", usertype="Personal")
            res = conn.execute("SELECT * FROM `user` where `id` = 'CYYoung'").fetchall()
            # print(res)
            self.assertEqual([], res)

    def test_update_user_some_info_none(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            origin = conn.execute("SELECT * FROM `user` where `id` = 'test2'").fetchall()
            utils.db.update_user("test2")
            res = conn.execute("SELECT * FROM `user` where `id` = 'test2'").fetchall()
            # print(res)
            self.assertEqual(origin[-1]['name'], res[-1]['name'])
            self.assertEqual(origin[-1]['email'], res[-1]['email'])
            self.assertEqual(origin[-1]['profile_pic'], res[-1]['profile_pic'])
            self.assertEqual(origin[-1]['usertype'], res[-1]['usertype'])

    def test_insert_audience_comment(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_audience_comment("Jason", "Alice", "Hello, World!")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * FROM audience_comment where watcher = 'Jason'").fetchall()
            self.assertEqual("Jason", res[-1]['watcher'])
            self.assertEqual("Alice", res[-1]['streamer'])
            self.assertEqual("Hello, World!", res[-1]['message'])

    def test_get_audience_comment(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_audience_comment("Jason", "Alice", "Hello, World!")
            utils.db.get_audience_comment("Alice")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * FROM audience_comment where streamer = 'Alice'").fetchall()
            self.assertEqual("Jason", res[-1]['watcher'])
            self.assertEqual("Alice", res[-1]['streamer'])
            self.assertEqual("Hello, World!", res[-1]['message'])

    def test_get_audience_comment_miss(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_audience_comment("Jason", "Alice", "Hello, World!")
            utils.db.get_audience_comment("Jason")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * FROM audience_comment where streamer = 'Jason'").fetchall()
            self.assertEqual([], res)

    def test_insert_advertise(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_advertise("Sony", "Gaming", "2099-11-11 11:11:11.111", "cool.png")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * FROM advertise").fetchall()
            self.assertEqual("Sony", res[-1]['streamer'])

    def test_insert_advertise_miss(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_advertise(None, "Gaming", "2099-11-11 11:11:11.111", "cool.png")
            conn = utils.db.get_db()
            res = conn.execute("SELECT * FROM advertise where image = 'cool.png'").fetchall()
            self.assertEqual([], res)

    def test_get_advertise(self):
        app = Flask(__name__)
        with app.app_context():
            res = utils.db.get_advertise("test3")
            # print(res)
            self.assertEqual("\\static\\Puppy-Class-ad.jpg", res[0])

    def test_get_advertise_over_time(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_advertise("Sony", "Gaming", "2011-11-11 11:11:11.111", "cool.png")
            utils.db.create_stream("Sony", "Sony", "Gaming")
            res = utils.db.get_advertise("Sony")
            # print(res)
            self.assertEqual("/static/simple-background-backgrounds-passion-simple-1-5c9b95d09002a.png", res[0])

    def test_get_advertise_over_time_miss(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_advertise("Sony", "Gaming", "2011-11-11 11:11:11.111", "cool.png")
            #utils.db.create_stream("Sony", "Sony", "Gaming")
            res = utils.db.get_advertise("Sony")
            # print(res)
            self.assertEqual([], res)

    def test_get_advertise_over_time_no_same_cat_ad(self):
        app = Flask(__name__)
        with app.app_context():
            utils.db.insert_advertise("Sony", "Gaming", "2011-11-11 11:11:11.111", "cool.png")
            conn = utils.db.get_db()
            conn.execute("DELETE from advertise")
            utils.db.create_stream("Sony", "Sony", "Gaming")
            res = utils.db.get_advertise("Sony")
            # print(res)
            self.assertEqual([], res)

    def test_get_advertise_over_time_no_same_cat(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from advertise")
            utils.db.insert_advertise("Sony", "Gaming", "2011-11-11 11:11:11.111", "cool.png")
            utils.db.create_stream("Sony", "Sony", "Gaming")
            res = utils.db.get_advertise("Sony")
            # print(res)
            self.assertEqual([], res)

    def test_get_advertise_streamer_none(self):
        app = Flask(__name__)
        with app.app_context():
            conn = utils.db.get_db()
            conn.execute("DELETE from advertise")
            res = utils.db.get_advertise()
            self.assertEqual([], res)

    def test_create_user(self):
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

    def test_create_user_miss(self):
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

    def test_get_user(self):
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

    def test_get_user_miss(self):
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

    # make sure any test never affect the application or other tests in db.
    def tearDown(self):
        os.system("git restore utils/sqlite_db")
        print("tearDown")

