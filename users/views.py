import jwt, requests

from django.views     import View
from django.http      import JsonResponse
from django.conf      import settings

from users.models     import User
        
def get_user_information(access_token):
    header = {
        "Authorization" : f'Bearer {access_token}',
        "Content-type"  : "application/x-www-form-unlencoded;charset=utf-8"
    }
    user_info = requests.get("https://kapi.kakao.com/v2/user/me", headers = header, timeout = 10)
    
    return user_info.json()
        
    
class KakaoSignView(View):
    def get(self, request):
        token     = request.headers.get('Authorization', None)
        user_info = get_user_information(token)
        kakao_id  = user_info['id']
        nickname  = user_info['kakao_account']['profile']['nickname']
        email     = user_info['kakao_account']['email']
        
        user, created = User.objects.get_or_create(
            kakao_id = kakao_id, defaults = {'name' : nickname, 'email' : email}
            )   
             
        token = jwt.encode({'id':user.id}, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        if created:
            return JsonResponse({"message" : "CREATED", "token" : token}, status = 201)
        
        return JsonResponse({"message" : "SIGNED_IN", "token" : token}, status = 200)