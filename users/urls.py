from django.urls    import path
from users.views import KakaoSigninView, GetUserInfoView

urlpatterns = [
    path('/kakao/callback', GetUserInfoView.as_view()),
    path('/kakao', KakaoSigninView.as_view()),   
]