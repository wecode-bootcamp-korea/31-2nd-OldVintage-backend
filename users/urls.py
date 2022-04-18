from django.urls  import path
from users.views  import KakaoSignView

urlpatterns = [
    path('/kakao', KakaoSignView.as_view())
]