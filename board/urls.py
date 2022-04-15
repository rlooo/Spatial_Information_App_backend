from django.urls import path
from board import views
from board.views import *

# 이미지 업로드
from django.conf.urls.static import static
from django.conf import settings

app_name = 'board'
urlpatterns = [

    # Example: /board/new_post/put_out/
    path('new_post/put_out/', new_post, name='new_post'),
    #
    # # Example: /board/1/detail/
    # path('<int:pk>/detail/', views.board_detail, name="post_detail"),
    #
    # # Example: /board/1/modify/
    # path('<int:pk>/modify/', views.post_modify, name='post_modify'),
    #
    # # Example: /board/1/delete/
    # path('<int:pk>/delete/', views.post_delete, name='post_delete'),

]
# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
