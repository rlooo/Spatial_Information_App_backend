from django.urls import path
from board.views import *

# 이미지 업로드
from django.conf.urls.static import static
from django.conf import settings

app_name = 'board'
urlpatterns = [

    # Example: /board/new_post/put_out/
    path('new_post/put_out2/', new_putout2, name='put_out'),

    # Example: /board/new_post/look_for/
    path('new_post/look_for/', new_lookfor, name='look_for'),

    # Example: /board/detail/1
    path('detail/<int:pk>/', putout_detail, name="putout_detail"),
    #
    # # Example: /board/1/modify/
    # path('<int:pk>/modify/', views.post_modify, name='post_modify'),
    #
    # Example: /board/delete/1
    path('delete/<int:pk>', putout_delete, name='putout_delete'),

    # Example: /board/list/
    path('list/', PutOutListView.as_view(), name='putout_list'),

    # Example: /board/opendata/
    path('opendata/', openAPIData),

    # Example: /board/new_post/applyspace/
    path('new_post/applyspace/', applySpace),

    # Example: /board/convertPNU/
    path('convertPNU/', convertPNU),

    # Example: /board/notice/list/
    path('notice/list/', NoticeListView.as_view()),

    # Example: /board/qna/list/
    path('qna/list/', QnAListView.as_view()),

    # Example: /board/new_post/qna/
    path('new_post/qna/', new_qna),

    # Example: /board/image/download/1
    path('iamge/download/<int:putout_id>/', ImageDownloadView.as_view(), name = "image_download"),

]
# 이미지 URL 설정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
