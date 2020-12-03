"""unit test for utils.user"""
import requests
from unittest import TestCase
import unittest
from app import app

class TestNewUser(TestCase):

    # def setUpClass(self):
    #
    #     app.run(ssl_context="adhoc", debug=True)

    def test_newuser(self):
        with app.test_client() as c:
            url = '/newuser'
            data = {"uid": "c12", "fullname": "Carbon", "email": "c12@gg.com", "profile_pic": "123.png"}
            thing = c.post(url, data=data)
            thing = c.get(url)
            # print(thing.data)

    def test_index(self):
        with app.test_client() as c:
            thing = c.get('/')
            url = '/testLogin'
            thing = c.get(url)
            thing = c.get('/')

    def test_logout(self):
        with app.test_client() as c:
            thing = c.get('/logout')
            thing = c.get('/testLogin')
            thing = c.get('/logout')