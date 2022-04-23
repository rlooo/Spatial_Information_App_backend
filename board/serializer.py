from rest_framework import serializers

# 화면에서 보여줄 필드 명시
from board.models import PutOutBoard


class PutOutListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PutOutBoard
        fields = ('id', 'address', 'kakaoLatitude', 'kakaoLongitude', 'area', 'floor', 'deposit', 'price', 'discussion', 'range',)

