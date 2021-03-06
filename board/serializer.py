from rest_framework import serializers

# 화면에서 보여줄 필드 명시
from board.models import PutOut, QnA, Notice, BuildingImage


class PutOutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutOut
        fields = ('id', 'address', 'kakaoLatitude', 'kakaoLongitude', 'area', 'floor', 'deposit', 'price', 'discussion', 'range', 'address', 'detailAddress','thumbnail')

class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'link', 'created_at')

class QnAListSerializer(serializers.ModelSerializer):
    author_name = serializers.ReadOnlyField(source='author.nickname')
    print(author_name)
    class Meta:
        model = QnA
        fields = ('id', 'title', 'content', 'created_at', 'answer', 'author_name')