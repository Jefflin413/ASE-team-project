"""unit test for app.py"""
from unittest import TestCase
from unittest.mock import patch
import unittest
import os
import app
from flask import Flask
from flask import g
import utils.db
import utils.user
from utils.user import User
from datetime import datetime

unittest.TestLoader.sortTestMethodsUsing = None

def recordedToken0():
    return {'access_token': 'ya29.a0AfH6SMCBj53EnwBIz4y3RiyqArQmS8WFgvx6jsXQ1CiFGlzmsUDaz2XLy3o2nMeg4mpMHQn-XYdqmZhwR5gVr9e3BjdL96F-uPYFlnf1aMo-qMPpClBrlIvnCZpsDV0S3oOMmkpOMGLGFuDmjrT2npF1VhQL8u6o2XvqRMJnipE', 'expires_in': 3599, 'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid', 'token_type': 'Bearer', 'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0Y2JhMjVlNTYzNjYwYTkwMDlkODIwYTFjMDIwMjIwNzA1NzRlODIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjMwOTY1OTk1MzItOHM5bjFnaGFscHRpYmZidnFubGFsYnY0cXZxNWRyazEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIzMjMwOTY1OTk1MzItOHM5bjFnaGFscHRpYmZidnFubGFsYnY0cXZxNWRyazEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDYwNTY4MDg1NDI4MTMxMDkwOTIiLCJlbWFpbCI6ImFiYzY3OHBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJ3UE5lLVRrUGhNMlNkR2xNejhhWVpBIiwibmFtZSI6IuW-kOW9peaXuyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLWZjSmJrZHRoX3NRL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FNWnV1Y2xDVDk2S3VMWlNiZ1F3aXVZcFBKZkVuSFZfRVEvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IuW9peaXuyIsImZhbWlseV9uYW1lIjoi5b6QIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2MDcyMDY4MzIsImV4cCI6MTYwNzIxMDQzMn0.RgwQPHUWxl38zPcv-54fgzIEYWpeYLAKy6aCavk5J4m__dzZcej3L0Vybzh5qaTWA62vc0o3Pq_VWKZcY9cVToilZHBD7_daZWPQYRQjP8A1bdQVZ0uxv1kXW387tf_pAIXA-QbHnZMMOoKLF5QtpWvXJOvV45cO30I89Z6aFGifx_PMwqk-hYpK5qlSA06a9dKw_Ra2sNiIYPUV2sbtp7zdcgGi79AUWp1A7N-BcX3Sbm0zslLW0BsOlVeCCGPkzM2TWiB59ULSWo1TKm_3syDf9aHdrDCpsKVU8-kn8qrGcB-HLYkl990PFLAN_cbxJx3S-GNGNGeA0MDccwLIBQ'}

def recordedUserinfo0():
    return {'sub': '104334166667515838627', 'name': 'Yen Min Hsu', 'given_name': 'Yen Min', 'family_name': 'Hsu', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14Gh3Dx16cpRDiHeb1ewC0STneZu2gd2UTkz8GmlS=s96-c', 'email': 'hym199584@gmail.com', 'email_verified': True, 'locale': 'en'}

def recordedToken1():
    return {'access_token': 'ya29.a0AfH6SMAcG9ULGUdJFi49gtPgldjkUWtb_UtKkBOPurZEVMOrz6wWtwbNqIDOjzW8ksEl1FMA7m_ZKZtO1sf16ZNoMJ4q5fC80E3sIbvPP-1IAmfg11fDkjle20hYwVZ9RXch-g7flodWNNBoo9JF6TuRvurdEpYq9sYGGsQXHJ8N', 'expires_in': 3599, 'scope': 'https://www.googleapis.com/auth/userinfo.profile openid https://www.googleapis.com/auth/userinfo.email', 'token_type': 'Bearer', 'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0Y2JhMjVlNTYzNjYwYTkwMDlkODIwYTFjMDIwMjIwNzA1NzRlODIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjMwOTY1OTk1MzItOHM5bjFnaGFscHRpYmZidnFubGFsYnY0cXZxNWRyazEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIzMjMwOTY1OTk1MzItOHM5bjFnaGFscHRpYmZidnFubGFsYnY0cXZxNWRyazEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDI4NTkzNzAyOTU5MzQxNjI5OTkiLCJoZCI6ImNvbHVtYmlhLmVkdSIsImVtYWlsIjoieWgzMzI4QGNvbHVtYmlhLmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJhdF9oYXNoIjoic0VpeEczSXQ4S0J6ZVlsT2tFXzNkdyIsIm5hbWUiOiJZZW4tTWluIEhzdSIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS0vQU9oMTRHakpsT1J4SzBneVpSUmFWNS1rRzc3UV81NHpNeEpwejVOSU1LUEM9czk2LWMiLCJnaXZlbl9uYW1lIjoiWWVuLU1pbiIsImZhbWlseV9uYW1lIjoiSHN1IiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2MDcyNzE4MjIsImV4cCI6MTYwNzI3NTQyMn0.mQsmp-2nJojmMlTmZSBLhMaezRIfBKwftL-SoD6szMLZGV6eOIJZ4Kiaj3kQpKiCppKFxnIQOAXteCzlOZffOGDy7GCheSGGlpDrO9KSfQzsFSlbrDBPkBdmNEqLs17TD4NQd1hUVr-fYZy1QfghJmqq37wPrOxPU752ssoU1coBMIhjEiPASraRnzICXf2KQYa0jTX4Qqz5fpOMVqwJ-LgFIxoae_NMTyEKZSWI3-kQtY0fLaoHDlX1RFHG56ALIWCWwzA6XcDUBzR9jd3oSFn3xfv-ZXWb4QwZiNRlGjWeBok4iJ3AnROjI54UrZ9iCtzfhrOmFO7DqVDAstXPzg'}

def recordedUserinfoSuccess():
    return {'sub': '102859370295934162999', 'name': 'Yen-Min Hsu', 'given_name': 'Yen-Min', 'family_name': 'Hsu', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14GjJlORxK0gyZRRaV5-kG77Q_54zMxJpz5NIMKPC=s96-c', 'email': 'yh3328@columbia.edu', 'email_verified': True, 'locale': 'en', 'hd': 'columbia.edu'}

def recordedUserinfoInvalid():
    return {'error': 'invalid_request', 'error_description': 'Invalid Credentials'}

def recordedUserinfoExist():
    return {'sub': 'test1', 'name': 'Yen-Min Hsu', 'given_name': 'Yen-Min', 'family_name': 'Hsu', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14GjJlORxK0gyZRRaV5-kG77Q_54zMxJpz5NIMKPC=s96-c', 'email': 'yh3328@columbia.edu', 'email_verified': True, 'locale': 'en', 'hd': 'columbia.edu'}

def recordedGoogleProviderCfg():
    return {'issuer': 'https://accounts.google.com', 'authorization_endpoint': 'https://accounts.google.com/o/oauth2/v2/auth', 'device_authorization_endpoint': 'https://oauth2.googleapis.com/device/code', 'token_endpoint': 'https://oauth2.googleapis.com/token', 'userinfo_endpoint': 'https://openidconnect.googleapis.com/v1/userinfo', 'revocation_endpoint': 'https://oauth2.googleapis.com/revoke', 'jwks_uri': 'https://www.googleapis.com/oauth2/v3/certs', 'response_types_supported': ['code', 'token', 'id_token', 'code token', 'code id_token', 'token id_token', 'code token id_token', 'none'], 'subject_types_supported': ['public'], 'id_token_signing_alg_values_supported': ['RS256'], 'scopes_supported': ['openid', 'email', 'profile'], 'token_endpoint_auth_methods_supported': ['client_secret_post', 'client_secret_basic'], 'claims_supported': ['aud', 'email', 'email_verified', 'exp', 'family_name', 'given_name', 'iat', 'iss', 'locale', 'name', 'picture', 'sub'], 'code_challenge_methods_supported': ['plain', 'S256'], 'grant_types_supported': ['authorization_code', 'refresh_token', 'urn:ietf:params:oauth:grant-type:device_code', 'urn:ietf:params:oauth:grant-type:jwt-bearer']}



class TestApp(TestCase):

    def setUp(self):
        os.system("git restore utils/sqlite_db")
        print("setUp")

    def test_callback(self):
        self.patcher1 = patch('app.Google_client.prepare_token_request',
            new=unittest.mock.MagicMock(side_effect=[("https://oauth2.googleapis.com/token",
                {'Content-Type': 'application/x-www-form-urlencoded'},
                 "grant_type=authorization_code&client_id=323096599532-8s9n1ghalptibfbvqnlalbv4qvq5drk1.apps.googleusercontent.com&code=4%2F0AY0e-g7IjfKzSaWnM6tC0QArd3Cr1RstAitsdjyQPTtFSWTwjej_jKnhidJBQy5N0X5Inw&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2Flogin%2Fcallback")]))

        mockJson = unittest.mock.MagicMock(side_effect=recordedToken0)
        mockTokenResponse = unittest.mock.MagicMock()
        mockTokenResponse.json = mockJson
        self.patcher2 = patch("requests.post",
            new=unittest.mock.MagicMock(side_effect=[mockTokenResponse]))

        self.patcher3 = patch("app.get_google_provider_cfg",
                new=recordedGoogleProviderCfg)

        mockUserinfo = unittest.mock.MagicMock(side_effect=recordedUserinfoSuccess)
        mockUserinfoResponse = unittest.mock.MagicMock()
        mockUserinfoResponse.json = mockUserinfo
        self.patcher4 = patch("requests.get",
            new=unittest.mock.MagicMock(side_effect=[mockUserinfoResponse]))

        self.patcher1.start()
        self.patcher2.start()
        self.patcher3.start()
        self.patcher4.start()
        self.addCleanup(self.patcher1.stop)
        self.addCleanup(self.patcher2.stop)
        self.addCleanup(self.patcher3.stop)
        self.addCleanup(self.patcher4.stop)
        with app.app.test_client() as c:
            recorded_url = "/login/callback?code=4%2F0AY0e-g7IjfKzSaWnM6tC0QArd3Cr1RstAitsdjyQPTtFSWTwjej_jKnhidJBQy5N0X5Inw&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&authuser=3&prompt=consen"
            self.assertEqual(c.get(recorded_url).status_code, 200)

    def test_callback_exist(self):
        self.patcher1 = patch('app.Google_client.prepare_token_request',
            new=unittest.mock.MagicMock(side_effect=[("https://oauth2.googleapis.com/token",
                {'Content-Type': 'application/x-www-form-urlencoded'},
                 "grant_type=authorization_code&client_id=323096599532-8s9n1ghalptibfbvqnlalbv4qvq5drk1.apps.googleusercontent.com&code=4%2F0AY0e-g7IjfKzSaWnM6tC0QArd3Cr1RstAitsdjyQPTtFSWTwjej_jKnhidJBQy5N0X5Inw&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2Flogin%2Fcallback")]))

        mockJson = unittest.mock.MagicMock(side_effect=recordedToken0)
        mockTokenResponse = unittest.mock.MagicMock()
        mockTokenResponse.json = mockJson
        self.patcher2 = patch("requests.post",
            new=unittest.mock.MagicMock(side_effect=[mockTokenResponse]))

        self.patcher3 = patch("app.get_google_provider_cfg",
                new=recordedGoogleProviderCfg)

        mockUserinfo = unittest.mock.MagicMock(side_effect=recordedUserinfoExist)
        mockUserinfoResponse = unittest.mock.MagicMock()
        mockUserinfoResponse.json = mockUserinfo
        self.patcher4 = patch("requests.get",
            new=unittest.mock.MagicMock(side_effect=[mockUserinfoResponse]))

        self.patcher1.start()
        self.patcher2.start()
        self.patcher3.start()
        self.patcher4.start()
        self.addCleanup(self.patcher1.stop)
        self.addCleanup(self.patcher2.stop)
        self.addCleanup(self.patcher3.stop)
        self.addCleanup(self.patcher4.stop)
        with app.app.test_client() as c:
            recorded_url = "/login/callback?code=4%2F0AY0e-g7IjfKzSaWnM6tC0QArd3Cr1RstAitsdjyQPTtFSWTwjej_jKnhidJBQy5N0X5Inw&scope=email+profile+openid+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email+https%3A%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&authuser=3&prompt=consen"
            self.assertEqual(c.get(recorded_url).status_code, 302)

    def test_callback_invalid(self):
        self.patcher1 = patch('app.Google_client.prepare_token_request',
            new=unittest.mock.MagicMock(side_effect=[("https://oauth2.googleapis.com/token",
                {'Content-Type': 'application/x-www-form-urlencoded'},
                 "grant_type=authorization_code&client_id=323096599532-8s9n1ghalptibfbvqnlalbv4qvq5drk1.apps.googleusercontent.com&code=4%2F0AY0e-g5OcyfcnNxhH_Ne5cn77zZmyN7x9qwlJKD-KTYmOEMC63Irk_kNOYOudKSEIwWDrA&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2Flogin%2Fcallback")]))

        mockJson = unittest.mock.MagicMock(side_effect=recordedToken1)
        mockTokenResponse = unittest.mock.MagicMock()
        mockTokenResponse.json = mockJson
        self.patcher2 = patch("requests.post",
            new=unittest.mock.MagicMock(side_effect=[mockTokenResponse]))

        self.patcher3 = patch("app.get_google_provider_cfg",
                new=recordedGoogleProviderCfg)

        mockUserinfo = unittest.mock.MagicMock(side_effect=recordedUserinfoInvalid)
        mockUserinfoResponse = unittest.mock.MagicMock()
        mockUserinfoResponse.json = mockUserinfo
        self.patcher4 = patch("requests.get",
            new=unittest.mock.MagicMock(side_effect=[mockUserinfoResponse]))

        self.patcher1.start()
        self.patcher2.start()
        self.patcher3.start()
        self.patcher4.start()
        self.addCleanup(self.patcher1.stop)
        self.addCleanup(self.patcher2.stop)
        self.addCleanup(self.patcher3.stop)
        self.addCleanup(self.patcher4.stop)

        with app.app.test_client() as c:
            recorded_url = "/login/callback?code=4%2F0AY0e-g5OcyfcnNxhH_Ne5cn77zZmyN7x9qwlJKD-KTYmOEMC63Irk_kNOYOudKSEIwWDrA&scope=email%20profile%20openid%20https:%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.email%20https:%2F%2Fwww.googleapis.com%2Fauth%2Fuserinfo.profile&authuser=0&hd=columbia.edu&prompt=none"
            self.assertEqual(c.get(recorded_url).status_code, 400)

class TestNewUser(TestCase):

    def setUp(self):
        os.system("git restore utils/sqlite_db")
        print("setUp")
    # def setUpClass(self):
    #
    #     app.run(ssl_context="adhoc", debug=True)
    def test_newuser(self):
        with app.app.test_client() as c:
            url = '/newuser'
            data = {"uid": "101034240973870390330", "fullname": "Carbon", "email": "c12@gg.com", "profile_pic": "123.png", "usertype": "Company"}
            thing = c.post(url, data=data)
            thing = c.get(url)
            # print(thing.data)

    def test_index(self):
        with app.app.test_client() as c:
            thing = c.get('/')
            url = '/testLogin'
            thing = c.get(url)
            thing = c.get('/')

    def test_logout(self):
        with app.app.test_client() as c:
            thing = c.get('/logout')
            thing = c.get('/testLogin')
            thing = c.get('/logout')

    def test_login(self):
        with app.app.test_client() as c:
            c.get('/login')
            c.get('/testLogin')
            c.get('/testLogin')
            c.get('/test')
            c.get('/profile')

    def test_streaming(self):
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(side_effect=Exception()))
        patcher2 = patch('app.AWS_client.create_stack')
        patcher1.start()
        patcher2.start()
        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)

        with app.app.test_client() as c:
            c.get('/testLogin')
            data = {'stream_category': 'Life'}
            c.post('/stream', data=data)
            c.get('/stream')

    def test_streamingExist(self):
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock())
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            data = {'stream_category': 'Life'}
            c.post('/stream', data=data)

    def test_streamingFail(self):
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(side_effect=Exception()))
        patcher2 = patch('app.AWS_client.create_stack',
            new=unittest.mock.MagicMock(side_effect=Exception()))
        patcher1.start()
        patcher2.start()
        self.addCleanup(patcher1.stop)
        self.addCleanup(patcher2.stop)

        with app.app.test_client() as c:
            c.get('/testLogin')
            data = {'stream_category': 'Life'}
            c.post('/stream', data=data)

    def test_streamingDelete(self):
        patcher1 = patch('app.AWS_client.delete_stack')
        patcher1.start()
        self.addCleanup(patcher1.stop)

        with app.app.test_client() as c:
            c.get('/testLogin')
            c.post('/stream')

    def test_editprofile(self):
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/editprofile')

    def test_stream_describe_stack(self):
        mockStackDetail = {'Stacks':[{'StackStatus': 'CREATE_COMPLETE', 'Outputs':[0,0,{'OutputValue':['obsurl',6,5,4,3,2,1]}]}]}
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(return_value=mockStackDetail))
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/stream/describe_stack')

    def test_stream_describe_in_progress(self):
        mockStackDetail = {'Stacks':[{'StackStatus': 'IN_PROGRESS', 'Outputs':[0,0,{'OutputValue':['obsurl',6,5,4,3,2,1]}]}]}
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(return_value=mockStackDetail))
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/stream/describe_stack')

    def test_stream_delete(self):
        mockStackDetail = {'Stacks':[{'StackStatus': 'DELETE_IN_PROGRESS'}]}
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(return_value=mockStackDetail))
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/stream/describe_stack')

    def test_stream_yet(self):
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(side_effect=Exception()))
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/stream/describe_stack')

    def test_stream_show_video_player(self):
        mockStackDetail = {'Stacks':[{'StackStatus': 'CREATE_COMPLETE', 'Outputs':[0,0,{'OutputValue':['obsurl',6,5,4,3,2,1]},0,{'OutputValue': 'm3u8_URL'}]}]}
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(return_value=mockStackDetail))
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/stream/show_video_player')

    def test_stream_show_video_player_in_progress(self):
        mockStackDetail = {'Stacks':[{'StackStatus': 'IN_PROGRESS', 'Outputs':[0,0,{'OutputValue':['obsurl',6,5,4,3,2,1]},0,{'OutputValue': 'm3u8_URL'}]}]}
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(return_value=mockStackDetail))
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/stream/show_video_player')

    def test_stream_show_video_player_yet(self):
        patcher1 = patch('app.AWS_client.describe_stacks',
            new=unittest.mock.MagicMock(side_effect=Exception()))
        patcher1.start()
        self.addCleanup(patcher1.stop)
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/stream/show_video_player')

    def test_view_id(self):
        with app.app.test_client() as c:
            c.get("/view/test1")
            c.get('/testLogin')
            c.get("/view/test1")

    def test_company(self):
        with app.app.test_client() as c:
            c.get('/testLogin')
            c.get('/company/category')
        with app.app.test_client() as c:
            url = '/newuser'
            data = {"uid": "101034240973870390330", "fullname": "Carbon", "email": "c12@gg.com", "profile_pic": "123.png", "usertype": "Company"}
            c.post(url, data=data)
            c.get('/company/category')
            c.post('/company/category', data={'category':'education'})
            c.get('/company/user')
            c.post('/company/user', data={'category':'test1'})

    def test_payment(self):
        with app.app.test_client() as c:
            url = '/newuser'
            data = {"uid": "101034240973870390330", "fullname": "Carbon", "email": "c12@gg.com", "profile_pic": "123.png", "usertype": "Company"}
            c.post(url, data=data)
            data = {'Gaming': '124', 'Life': '2312', 'Sports': '', 'sports': '', 'education': ''}
            c.post('/payment', data=data)

    def test_thanks(self):
        with app.app.test_client() as c:
            url = '/newuser'
            data = {"uid": "101034240973870390330", "fullname": "Carbon", "email": "c12@gg.com", "profile_pic": "123.png", "usertype": "Company"}
            c.post(url, data=data)
            files = open('testpayment.png', 'rb')
            data = {'creditcard': '2133', 'Gaming': '124', 'Life': '2312','image': files}
            # files = {'image': open('testpayment.png', 'rb')}
            c.post('/thanks', data=data)
    def test_socket(self):
        # log the user in through Flask test client
        flask_test_client = app.app.test_client()

        # connect to Socket.IO without being logged in
        socketio_test_client = app.socketio.test_client(
            app.app, flask_test_client=flask_test_client)
        flask_test_client.get('/testLogin')
        print(dir(socketio_test_client))
        # connect to Socket.IO again, but now as a logged in user
        data = {'username': 'Alice', 'room': 'test1'}
        socketio_test_client.emit('join_room', data)
        data = {'username': 'Alice', 'room': 'test1', 'message': 'no more late days!'}
        socketio_test_client.emit('send_message', data)
        data = {'username': 'Alice', 'room': 'test1', 'UUID': 'b90746ee-35e7-11eb-9844-0e6eb579fb2b'}
        socketio_test_client.emit('leave_room', data)
        data = {'username': False, 'room': 'test1', 'UUID': 'b90746ee-35e7-11eb-9844-0e6eb579fb2b'}
        socketio_test_client.emit('leave_room', data)

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

if __name__ == "__main__":
    unittest.main()