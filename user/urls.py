from django.urls import path
from user.views import *

app_name = 'user'
urlpatterns = [
    # Example: /user/login/kakao/
    path('kakao/login/', login),
]