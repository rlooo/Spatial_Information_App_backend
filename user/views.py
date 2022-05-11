# 회원가입
from django.http import HttpResponse

from user.models import Account


def login(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')

    if Account.objects.filter(uid=uid).exists():
        user = Account.objects.get(uid=uid)
        return HttpResponse(status=200)

    user = Account.objects.create(
        uid=uid,
        email=email,
        nickname=nickname
    )

    user.save()
    return HttpResponse(status=200)

