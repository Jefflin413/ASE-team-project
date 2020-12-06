"""unit test for app.py"""
from unittest import TestCase
from unittest.mock import patch
import unittest
import requests
import time
from multiprocessing import Process
import app
unittest.TestLoader.sortTestMethodsUsing = None

def recordedToken():
    return {'access_token': 'ya29.a0AfH6SMCBj53EnwBIz4y3RiyqArQmS8WFgvx6jsXQ1CiFGlzmsUDaz2XLy3o2nMeg4mpMHQn-XYdqmZhwR5gVr9e3BjdL96F-uPYFlnf1aMo-qMPpClBrlIvnCZpsDV0S3oOMmkpOMGLGFuDmjrT2npF1VhQL8u6o2XvqRMJnipE', 'expires_in': 3599, 'scope': 'https://www.googleapis.com/auth/userinfo.profile https://www.googleapis.com/auth/userinfo.email openid', 'token_type': 'Bearer', 'id_token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6ImQ0Y2JhMjVlNTYzNjYwYTkwMDlkODIwYTFjMDIwMjIwNzA1NzRlODIiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20iLCJhenAiOiIzMjMwOTY1OTk1MzItOHM5bjFnaGFscHRpYmZidnFubGFsYnY0cXZxNWRyazEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJhdWQiOiIzMjMwOTY1OTk1MzItOHM5bjFnaGFscHRpYmZidnFubGFsYnY0cXZxNWRyazEuYXBwcy5nb29nbGV1c2VyY29udGVudC5jb20iLCJzdWIiOiIxMDYwNTY4MDg1NDI4MTMxMDkwOTIiLCJlbWFpbCI6ImFiYzY3OHBAZ21haWwuY29tIiwiZW1haWxfdmVyaWZpZWQiOnRydWUsImF0X2hhc2giOiJ3UE5lLVRrUGhNMlNkR2xNejhhWVpBIiwibmFtZSI6IuW-kOW9peaXuyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vLWZjSmJrZHRoX3NRL0FBQUFBQUFBQUFJL0FBQUFBQUFBQUFBL0FNWnV1Y2xDVDk2S3VMWlNiZ1F3aXVZcFBKZkVuSFZfRVEvczk2LWMvcGhvdG8uanBnIiwiZ2l2ZW5fbmFtZSI6IuW9peaXuyIsImZhbWlseV9uYW1lIjoi5b6QIiwibG9jYWxlIjoiZW4iLCJpYXQiOjE2MDcyMDY4MzIsImV4cCI6MTYwNzIxMDQzMn0.RgwQPHUWxl38zPcv-54fgzIEYWpeYLAKy6aCavk5J4m__dzZcej3L0Vybzh5qaTWA62vc0o3Pq_VWKZcY9cVToilZHBD7_daZWPQYRQjP8A1bdQVZ0uxv1kXW387tf_pAIXA-QbHnZMMOoKLF5QtpWvXJOvV45cO30I89Z6aFGifx_PMwqk-hYpK5qlSA06a9dKw_Ra2sNiIYPUV2sbtp7zdcgGi79AUWp1A7N-BcX3Sbm0zslLW0BsOlVeCCGPkzM2TWiB59ULSWo1TKm_3syDf9aHdrDCpsKVU8-kn8qrGcB-HLYkl990PFLAN_cbxJx3S-GNGNGeA0MDccwLIBQ'}

def recordedUserinfo():
    return {'sub': '104334166667515838627', 'name': 'Yen Min Hsu', 'given_name': 'Yen Min', 'family_name': 'Hsu', 'picture': 'https://lh3.googleusercontent.com/a-/AOh14Gh3Dx16cpRDiHeb1ewC0STneZu2gd2UTkz8GmlS=s96-c', 'email': 'hym199584@gmail.com', 'email_verified': True, 'locale': 'en'}

def recordedGoogleProviderCfg():
    return {'issuer': 'https://accounts.google.com', 'authorization_endpoint': 'https://accounts.google.com/o/oauth2/v2/auth', 'device_authorization_endpoint': 'https://oauth2.googleapis.com/device/code', 'token_endpoint': 'https://oauth2.googleapis.com/token', 'userinfo_endpoint': 'https://openidconnect.googleapis.com/v1/userinfo', 'revocation_endpoint': 'https://oauth2.googleapis.com/revoke', 'jwks_uri': 'https://www.googleapis.com/oauth2/v3/certs', 'response_types_supported': ['code', 'token', 'id_token', 'code token', 'code id_token', 'token id_token', 'code token id_token', 'none'], 'subject_types_supported': ['public'], 'id_token_signing_alg_values_supported': ['RS256'], 'scopes_supported': ['openid', 'email', 'profile'], 'token_endpoint_auth_methods_supported': ['client_secret_post', 'client_secret_basic'], 'claims_supported': ['aud', 'email', 'email_verified', 'exp', 'family_name', 'given_name', 'iat', 'iss', 'locale', 'name', 'picture', 'sub'], 'code_challenge_methods_supported': ['plain', 'S256'], 'grant_types_supported': ['authorization_code', 'refresh_token', 'urn:ietf:params:oauth:grant-type:device_code', 'urn:ietf:params:oauth:grant-type:jwt-bearer']}

class TestApp(TestCase):
    # @classmethod
    # def setUpClass(cls):
    #     pass
    def test_callback(self):
        self.patcher1 = patch('app.Google_client.prepare_token_request',
            new=unittest.mock.MagicMock(side_effect=[("https://oauth2.googleapis.com/token",
                {'Content-Type': 'application/x-www-form-urlencoded'},
                 "grant_type=authorization_code&client_id=323096599532-8s9n1ghalptibfbvqnlalbv4qvq5drk1.apps.googleusercontent.com&code=4%2F0AY0e-g7IjfKzSaWnM6tC0QArd3Cr1RstAitsdjyQPTtFSWTwjej_jKnhidJBQy5N0X5Inw&redirect_uri=https%3A%2F%2F127.0.0.1%3A5000%2Flogin%2Fcallback")]))

        mockJson = unittest.mock.MagicMock(side_effect=recordedToken)
        mockTokenResponse = unittest.mock.MagicMock()
        mockTokenResponse.json = mockJson
        self.patcher2 = patch("requests.post",
            new=unittest.mock.MagicMock(side_effect=[mockTokenResponse]))

        self.patcher3 = patch("app.get_google_provider_cfg",
                new=recordedGoogleProviderCfg)

        mockUserinfo = unittest.mock.MagicMock(side_effect=recordedUserinfo)
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
            c.get(recorded_url)

