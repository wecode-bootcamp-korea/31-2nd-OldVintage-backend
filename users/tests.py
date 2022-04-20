import jwt

from django.test         import TestCase, Client
from django.conf         import settings

from unittest.mock       import patch
from users.models        import User
from oldvintage.settings import SECRET_KEY, ALGORITHM

class KakaoSignTest(TestCase):
    def setUp(self):
        User.objects.create(
            id       = 1,
            kakao_id = 123456789,
            name     = "abc",
            email    = "abc@gmail.com"
        )
    
    def tearDown(self):
        User.objects.all().delete()
        
    @patch("users.views.requests.get")
    def test_kakao_signin_succes(self, mocked_kakao_user_info):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":123456789,
                    "properties": {
                            "nickname": "홍길동"
                    },
                    "kakao_account": { 
                        "profile" : {"nickname": "홍길동"},
                        "profile_needs_agreement": False,    
                        "email": "sample@sample.com"
                }}

        mocked_kakao_user_info.return_value = MockedResponse()

        headers  = {"Authorization": "가짜 access_token"}
        response = client.get("/users/kakao", **headers)
        
        user_id = jwt.decode(response.json()['token'], settings.SECRET_KEY, settings.ALGORITHM)
        token   = jwt.encode({'id':user_id['id']}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"message" : "SIGNED_IN", "token" : token})
        
    @patch("users.views.requests.get")
    def test_kakao_signup_success(self, mocked_kakao_user_info):
        client = Client()

        class MockedResponse:
            def json(self):
                return {
                    "id":1234567891,
                    "properties": {
                            "nickname": "홍길동"
                    },
                    "kakao_account": { 
                        "profile" : {"nickname": "홍길동"},
                        "profile_needs_agreement": False,    
                        "email": "sample@sample.com"
                }}

        mocked_kakao_user_info.return_value = MockedResponse()

        headers  = {"Authorization": "가짜 access_token"}
        response = client.get("/users/kakao", **headers)
        
        user_id = jwt.decode(response.json()['token'], settings.SECRET_KEY, settings.ALGORITHM)
        token   = jwt.encode({'id':user_id['id']}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"message" : "CREATED", "token" : token})
