"""unit test for app.py"""
import unittest
from unittest import TestCase
import requests
import sys
import os
import time
from unittest.mock import MagicMock
from multiprocessing import Process

os.chdir("../")
sys.modules['boto3'] = MagicMock()
from app import app
unittest.TestLoader.sortTestMethodsUsing = None


def f():
    """an ill-named wrapper for multiprocessing"""
    app.run(debug=True)


class TestApp(TestCase):
    @classmethod
    def setUpClass(cls):
        """once before all the tests"""
        p = Process(target=f)
        p.start()
        time.sleep(5)
        print("start test")

    def test_newuser(self):
        requests.get('http://127.0.0.1:5000/newuser')

    def test_profile(self):
        requests.get('http://127.0.0.1:5000/profile')

    def test_logout(self):
        requests.get('http://127.0.0.1:5000/logout')

    def test_login(self):
        requests.get('http://127.0.0.1:5000/login')

    def test_login_callback(self):
        requests.get('http://127.0.0.1:5000/login/callback')

    def test_stream(self):
        requests.get('http://127.0.0.1:5000/stream')

    def test_index(self):
        requests.get('http://127.0.0.1:5000/')


if __name__ == '__main__':
    unittest.main()
