from django.shortcuts import render, redirect

import json
import jwt
import requests

from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

import firebase_admin
from firebase_admin import auth as firebase_auth
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import auth

from django.views import View

from config.settings import SECRET_KEY # 배포 전 secret_key 옮기기
from .models import Account

@method_decorator(csrf_exempt, name='dispatch')
class KakaoSignInView(View):
    def get(self, request):
        redirectUri = request.GET.get('redirect-uri')

        app_key = '7f44810be24159eb8b2748926096d3d8'
        redirect_uri = 'http://10.0.2.2:8000/user/signin/kakao/token'
        kakao_auth_api = 'https://kauth.kakao.com/oauth/authorize?response_type=code'
        return redirect(
            f'{kakao_auth_api}&client_id={app_key}&redirect_uri={redirect_uri}'
        )
        # params = {'client_id': app_key, 'redirect_uri': redirect_uri}
        # kakao_response = requests.post(kakao_auth_api, params=params)
        # print(kakao_response)


@method_decorator(csrf_exempt, name='dispatch')
class KakaoSignInCallBackView(View):
    def get(self, request):
        auth_code = request.GET.get('code')

        kakao_token_api = 'https://kauth.kakao.com/oauth/token'
        data = {
            'grant_type': 'authorization_code',
            'client_id': '7f44810be24159eb8b2748926096d3d8',
            'redirection_uri': 'http://10.0.2.2:8000/user/signin/kakao/token',
            'code': auth_code,
        }

        token_response = requests.post(kakao_token_api, data=data)

        access_token = token_response.json().get('access_token')
        refresh_token = token_response.json().get('refresh_token')

        user_info_response = requests.get('https://kapi.kakao.com/v2/user/me', headers={"Authorization": f'Bearer {access_token}',"Content-type": "application/x-www-form-urlencoded; charset=utf-8"})
        user_info_json = json.loads(user_info_response.text)  # 유저의 정보를 json화해서 변수에 저장
        print(user_info_json)

        if Account.objects.filter(uid=user_info_json['id']).exists():
            user = Account.objects.get(uid=user_info_json['id'])

        else:
            user = Account(
                uid=user_info_json['id'],
                email=user_info_json['kakao_account'].get('email', None),
                nickname=user_info_json['properties'].get('nickname'),
                access_token = access_token,
                refresh_token = refresh_token,
            )
            user.save()

        # return JsonResponse({
        #     'id': user.uid,
        #     'email': user.email,
        #     'nickname': user.nickname,
        #     'access_token': access_token,
        #     'refresh_token' : refresh_token,
        # }, status=200)

        # 1. 사용자 정보로 파이어 베이스 유저정보 update, 사용자 정보가 있다면 userRecord에 유저 정보가 담긴다.
        ref = db.reference(user.uid)
        if ref is not None:
            ref.update({'email': user.email, 'nickname': user.nickname})
        else:
            ref.update({'uid': user.uid, 'email': user.email, 'emailVerified': False, 'nickname': user.nickname})  # 해당 변수가 없으면 생성한다.

        # 2. 전달받은 user 정보로 CustomToken을 발행한다.
        custom_token = auth.create_custom_token(user.uid)
        print(custom_token)

        # return JsonResponse({
        #     'custom_token': str(custom_token),
        # }, status=200)
        # return HttpResponseRedirect(reverse('webauthcallback://success?customToken='+str(custom_token)));
        # return redirect(reverse('webauthcallback://success?customToken='+str(custom_token)));
        params = {'custom_token': custom_token}
        requests.post('webauthcallback://success?', params=params)


@method_decorator(csrf_exempt, name='dispatch')
class CreateFirebaseCustomTokenView(View):
    def post(self, request):
        uid = request.GET.get('uid')
        email = request.Get.get('email')
        nickname = request.GET.GET('nickname')

        # uid = request.GET.get('id')
        # email = request.GET.get('email')
        # nickname = request.GET.get('nickname')

        # uid = data['id']
        # email = data['email']
        # nickname = data['nickname']


        # 1. 사용자 정보로 파이어 베이스 유저정보 update, 사용자 정보가 있다면 userRecord에 유저 정보가 담긴다.
        ref = db.reference(uid)
        if ref is not None:
            ref.update({'email': email, 'nickname': nickname})
        else:
            ref.update({'uid': uid, 'email': email, 'emailVerified': False, 'nickname': nickname}) # 해당 변수가 없으면 생성한다.

        # 2. 전달받은 user 정보로 CustomToken을 발행한다.
        custom_token = auth.create_custom_token(uid)
        print(custom_token)

        return JsonResponse({
            'custom_token': str(custom_token),
        }, status=200)


# @method_decorator(csrf_exempt, name='dispatch')
# class KakaoSignInView2(View):
#     def get(self, request):
#         data = json.loads(request.body)
#         customToken = data['custom_token']
#         return redirect(
#             f'{reverse("redirect:spartialDataInfraStructureScheme://success")}?customToken={customToken}'
#         )

@method_decorator(csrf_exempt, name='dispatch')
class KakaoLogoutView(View):
    def post(self, request):
        access_token = request.GET.get('access_token')
        response = requests.get('https://kapi.kakao.com/v1/user/logout',
                                          headers={"Authorization": f'Bearer {access_token}',
                                                   "Content-type": "application/x-www-form-urlencoded; charset=utf-8"})
        response_json = json.loads(response.text)
        print(response_json)
        return JsonResponse({
            'access_token': access_token,
        }, status=200)

