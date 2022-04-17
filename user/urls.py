from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    # Example: /user/signin/kakao/
    path('signin/kakao/', KakaoSignInView.as_view()),
    # path('signin/kakao/callback/', KakaoSignInCallBackView.as_view()),

    # Example: /user/signin/kakao/token/
    path('signin/kakao/token/', KakaoSignInCallBackView.as_view()),

    # Example: /user/signin/kakao/customtoken/
    path('signin/kakao/customtoken/', CreateFirebaseCustomTokenView.as_view()),

    path('logout/kakao/', KakaoLogoutView.as_view()),

    # path('signin2/kakao/', KakaoSignInView2.as_view()),
]