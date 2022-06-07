from rest_framework import serializers

# 화면에서 보여줄 필드 명시
from board.models import PutOut, QnA, Notice


class PutOutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutOut
        fields = ('id', 'address', 'kakaoLatitude', 'kakaoLongitude', 'area', 'floor', 'deposit', 'price', 'discussion', 'range', 'address', 'images', )

class NoticeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notice
        fields = ('id', 'title', 'content', 'created_at')

class QnAListSerializer(serializers.ModelSerializer):
    class Meta:
        model = QnA
        fields = ('id', 'title', 'content', 'created_at', 'answer')