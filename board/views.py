from django.http import HttpResponse
from django.shortcuts import render

import json

from board.models import Board

# Create your views here.
#새로운 게시글 작성하는 함수
from user.models import Account


def new_post(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        area = request.POST.get('area')
        floor = request.POST.get('floor')
        deposit = request.POST.get('deposit')
        price = request.POST.get('price')
        discussion = request.POST.get('discussion')
        client = request.POST.get('client')
        sort = request.POST.get('sort')
        count = request.POST.get('count')
        range = request.POST.get('range')
        print(discussion)
        # if Account.objects.filter(uid=uid).exists():
        #     user = Account.objects.get(uid=uid)

        new_article = Board.objects.create(
            # author=user,
            name=name,
            contact=contact,
            area=int(area),
            floor=int(floor),
            deposit=int(deposit),
            price=int(price),
            discussion=int(discussion),
            client = int(client),
            sort = int(sort),
            count =int(count),
            range = int(range),
        )

        new_article.save()

        return HttpResponse(status=200)


# # 게시글 삭제 기능
# #@id_auth
# def post_delete(request, pk):
#     # data = json.loads(request.body)
#     # login_session = data['login_session']
#     board = get_object_or_404(Board, id=pk)
#     # if board.author.social_login_id == login_session:
#     board.delete()
#     return HttpResponse(status=200)
#     # else:
#     #     return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
#
#
# # 게시글 수정 기능
# #@id_auth
# def post_modify(request, pk):
#     #data = json.loads(request.body)
#     # login_session = data['login_session']
#     board = get_object_or_404(Board, id=pk)
#
#     # if board.author.social_login_id != login_session:
#     #     return JsonResponse({'MESSAGE': 'INVALID_USER'}, status=401)
#
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         if Category.objects.filter(id=data['category']).exists():
#             category_obj = Category.objects.get(id=data['category'])
#
#         board.title = data['title']
#         board.text = data['text']
#         board.date = data['date']
#         board.longitude = data['longitude']
#         board.latitude = data['latitude']
#         board.price = data['price']
#         board.category = category_obj
#         board.thumbnail = data['thumbnail']
#
#         board.save()
#
#         return HttpResponse(status=200)
#
# # 게시물 상세 조회하는 함수
# def board_detail(request, pk):
#     # data = json.loads(request.body)
#     # login_session = data['login_session']
#
#     # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
#     board = get_object_or_404(Board, id=pk)
#
#     # # 글의 작성자인지 판별
#     # if board.author.social_login_id == login_session:
#     #     author_vaild = True
#     # else:
#     #     author_vaild = False
#
#     return HttpResponse(json.dumps(board, indent=4, sort_keys=True, default=str),
#                             content_type="application/json", status=200)