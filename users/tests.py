import jwt
from django.test         import TestCase, Client
from unittest.mock       import MagicMock, patch
from users.models        import User
from oldvintage.settings import SECRET_KEY, ALGORITHM

class KakaoSignUpTest(TestCase):
    @patch("users.views.requests.get")
    @patch("users.views.requests.post")
    def test_kakao_signin_new_user_success(self, mocked_token, mocked_kakao_user_info):
        client = Client()

        class FirstMockedResponse:
            def json(self):
                return {
                    "token_type":"bearer",
                    "access_token":"FAKE_ACCESS_TOKEN",
                    "expires_in":43199,
                    "refresh_token":"REFRESH_TOKEN",
                    "refresh_token_expires_in":25184000,
                    "scope":"account_email profile"
                        }
                
        class SecondMockedResponse:
            def json(self):
                return {
                    "id":123456789,
                    "properties": {
                            "nickname": "홍길동"
                    },
                    "kakao_account": { 
                        "nickname": "홍길동",
                        "profile_needs_agreement": False,    
                        "email": "sample@sample.com"
                }}

        mocked_token.return_value           = FirstMockedResponse()
        mocked_kakao_user_info.return_value = SecondMockedResponse()

        headers             = {"Authorization": "가짜 access_token"}
        response            = client.get("/users/kakao/callback", **headers)

        self.assertEqual(response.status_code, 201)



class KakaoSignInTest(TestCase):
    def setUp(self):
        User.objects.create(
            id=1,
            name = "홍길동",
            kakao_id = 123456789,
            email = "sample@sample.com"
        )
    
    @patch("users.views.requests.get")
    @patch("users.views.requests.post")
    def test_kakao_signin_registered_user_success(self, mocked_token, mocked_kakao_user_info):
        client = Client()

        class FirstMockedResponse:
            def json(self):
                return {
                    "token_type":"bearer",
                    "access_token":"FAKE_ACCESS_TOKEN",
                    "expires_in":43199,
                    "refresh_token":"REFRESH_TOKEN",
                    "refresh_token_expires_in":25184000,
                    "scope":"account_email profile"
                        }
                
        class SecondMockedResponse:
            def json(self):
                return {
                    "id":123456789,
                    "properties": {
                            "nickname": "홍길동"
                    },
                    "kakao_account": { 
                        "nickname": "홍길동",
                        "profile_needs_agreement": False,    
                        "email": "sample@sample.com"
                }}

        mocked_token.return_value           = FirstMockedResponse()
        mocked_kakao_user_info.return_value = SecondMockedResponse()

        headers             = {"Authorization": "가짜 access_token"}
        response            = client.get("/users/kakao/callback", **headers)

        self.assertEqual(response.status_code, 200)