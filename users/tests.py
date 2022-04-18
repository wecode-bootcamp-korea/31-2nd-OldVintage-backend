from django.test         import TestCase, Client
from unittest.mock       import patch
from users.models        import User

class KakaoSignUpTest(TestCase):
    @patch("users.views.requests.get")
    def test_kakao_signin_new_user_success(self, mocked_kakao_user_info):
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

        headers             = {"Authorization": "가짜 access_token"}
        response            = client.get("/users/kakao", **headers)

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
    def test_kakao_signin_registered_user_success(self, mocked_kakao_user_info):
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

        headers             = {"Authorization": "가짜 access_token"}
        response            = client.get("/users/kakao", **headers)

        self.assertEqual(response.status_code, 200)