import json, re, bcrypt, jwt, requests

from django.shortcuts import render, redirect
from django.views     import View
from django.http      import JsonResponse
from django.conf      import settings

from users.models     import User

class KakaoAPI:
    def __init__(self, authorization_code):
        self.authorization_code = authorization_code
        self.token_url          = "https://kauth.kakao.com/oauth/token"
        self.user_url           = "https://kapi.kakao.com/v2/user/me"
        self.redirect_url       = "http://10.58.3.235:8000/users/kakao/callback"
        
    def get_access_token(self):
        data = {
            'grant_type'  : 'authorization_code',
            'client_id'   : settings.KAKAO_APP_KEY,
            'redirect_uri': self.redirect_url,
            'code'        : self.authorization_code
        }
        response     = requests.post(self.token_url, data, timeout = 10)

        if not response.status_code == 200:
            return JsonResponse({'message' : 'TOKEN_TIMEOUT'}, status = 408)
        
        access_token = response.json()['access_token']
        return access_token
        
    def get_user_information(self, access_token):
        header = {
            "Authorization" : f'Bearer {access_token}',
            "Content-type"  : "application/x-www-form-unlencoded;charset=utf-8"
        }
        user_info = requests.get(self.user_url, headers = header, timeout = 10)
        
        if not user_info.status_code == 200:
            return JsonResponse({'message' : 'USER_INFO_TIMEOUT'}, status = 408)

        return user_info.json()
        
    
class KakaoSignView(View):
    def get(self, request):
        auth_code    = request.GET.get('code')
        kakao_api     = KakaoAPI(auth_code)
        access_token = kakao_api.get_access_token()
        user_info    = kakao_api.get_user_information(access_token)
        kakao_id     = user_info['id']
        nickname     = user_info['kakao_account']['profile']['nickname']
        email        = user_info['kakao_account']['email']
        
        user, created = User.objects.get_or_create(
            kakao_id = kakao_id, defaults = {'name' : nickname, 'email' : email}
            )   
             
        token = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

        if created:
            return JsonResponse({"message" : "CREATED", "token" : token}, status = 201)
        
        return JsonResponse({"message" : "SIGNED_IN", "token" : token}, status = 200)