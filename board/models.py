from django.db import models

# Create your models here.
from django.utils import timezone
from multiselectfield import MultiSelectField

from user.models import Account


class PutOutBoard(models.Model):
    DISCUSSION_CHOICES = [
        (1, '보증금/월세 협의 불가능'),
        (2, '보증금/월세 협의 가능'),
    ]

    CLIENT_CHOICES = [
        (1, '건물주'),
        (2, '가게주'),
    ]

    SORT_CHOICES = [
        (1, '전체'),
        (2, '월세'),
        (3, '전세'),
    ]

    COUNT_CHOICES = [
        (1, '1개'),
        (2, '2개'),
        (3, '3개+')
    ]

    RANGE_CHOICES = [
        (1, '상가, 점포로만 사용하는 게 좋아요'),
        (2, '상가, 점포와 사무실 둘 다 사용 가능해요'),
    ]

    FACILITY_CHOICES = [
        (1, '즉시 입주 가능'),
        (2, '내부 화장실'),
        (3, '남녀 화장실 구분'),
        (4, '개별난방'),
        (5, '엘리베이터'),
        (6, '최근 리모델링'),
        (7, '주차대수'),
        (8, '테라스'),
        (9, '루프탑'),
        (10, '샵인샵'),
        (11, '24시간 개방')
    ]

    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.SET_NULL)
    area = models.IntegerField()
    floor = models.IntegerField()
    deposit = models.IntegerField()
    price = models.IntegerField()
    discussion = models.PositiveSmallIntegerField(choices=DISCUSSION_CHOICES, null=True)  # 협의 가능 여부
    client = models.PositiveSmallIntegerField(choices=CLIENT_CHOICES, null=True)  # 의뢰인
    sort = models.PositiveSmallIntegerField(choices=SORT_CHOICES, null=True)  # 거래 종류
    count = models.PositiveSmallIntegerField(choices=COUNT_CHOICES, null=True)  # 공간 개수
    range = models.PositiveSmallIntegerField(choices=RANGE_CHOICES, null=True)  # 공간 사용 범위
    facility = MultiSelectField(choices=FACILITY_CHOICES, null=True)  # 시설 정보
    images = models.CharField(max_length=2000, null=True, blank=True) #건물 이미지
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "putout"

class LookForBoard(models.Model):
    DISCUSSION_CHOICES = [
        (1, '보증금/월세 협의 불가능'),
        (2, '보증금/월세 협의 가능'),
    ]

    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.SET_NULL)
    business = models.CharField(max_length=50)
    area = models.IntegerField()
    deposit = models.IntegerField()
    price = models.IntegerField()
    discussion = models.PositiveSmallIntegerField(choices=DISCUSSION_CHOICES, null=True)  # 협의 가능 여부
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lookfor"


class Address(models.Model):
    postCode = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    kakaoLatitude = models.CharField(max_length=50)
    kakaoLongitude = models.CharField(max_length=50)

    class Meta:
        db_table = "addresses"

