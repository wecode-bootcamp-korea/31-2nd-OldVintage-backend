import json, re, bcrypt, jwt, requests

from django.shortcuts import render, redirect
from django.views     import View
from django.http      import JsonResponse
from django.conf      import settings

from users.models     import User

class KakaoSigninView(View):
    def get(self, request):
        redirect_uri = 'http://10.58.4.34:8000/users/kakao/callback'
        kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'

        return redirect(
            f'{kakao_auth_api}&client_id={settings.KAKAO_APP_KEY}&redirect_uri={redirect_uri}'
        )
    
class GetUserInfoView(View):
    def get(self, request):
        code            = request.GET.get('code')
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        
        data = {
            'grant_type': 'authorization_code',
            'client_id': settings.KAKAO_APP_KEY,
            'redirect_uri': 'http://10.58.4.34:8000/users/kakao/callback',
            'code': code
        }
        response       = requests.get(kakao_token_api, data)
        access_token   = response.json().get('access_token')
        kakao_user_api = "https://kapi.kakao.com/v2/user/me"
        
        header = {
            "Authorization" : f'Bearer {access_token}',
            "Content-type" : "application/x-www-form-unlencoded;charset=utf-8"
        }

        user_info = requests.get(kakao_user_api, headers = header).json()
        kakao_id  = user_info.get('id')
        nickname  = user_info.get('properties')['nickname']
        email     = user_info.get('kakao_account')['email']

        user, created = User.objects.get_or_create(
            kakao_id = kakao_id, defaults = {'name' : nickname, 'email':email}
            )

        token = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        if created:
            return JsonResponse({"message" : "CREATED", "token" : token}, status = 201)

        return JsonResponse({"message" : "SIGNED_IN", "token" : token}, status = 200)
