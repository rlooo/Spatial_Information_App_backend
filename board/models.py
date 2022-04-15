
from django.db import models

# Create your models here.
from django.utils import timezone

from user.models import Account


class Board(models.Model):
    CLIENT_CHOICES = [
        (1, '건물주'),
        (2, '가게주'),
    ]

    SORT_CHOICES = [
        (1, '전체'),
        (2, '월세'),
        (3, '전세'),
    ]

    RANGE_CHOICES = [
        (1, '상가, 점포로만 사용하는 게 좋아요'),
        (2, '상가, 점포와 사무실 둘 다 사용 가능해요'),
    ]

    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.ForeignKey('Address', null=True, blank=True, on_delete=models.SET_NULL)
    area = models.IntegerField()
    floor = models.IntegerField()
    deposit = models.IntegerField()
    price = models.IntegerField()
    discussion = models.CharField(max_length=50) # 협의 가능 여부
    client = models.PositiveSmallIntegerField(choices=CLIENT_CHOICES, null=True) # 의뢰인
    sort = models.PositiveSmallIntegerField(choices=SORT_CHOICES, null=True) # 거래 종류
    count = models.IntegerField(null=True) # 공간 개수
    range = models.PositiveSmallIntegerField(choices=RANGE_CHOICES, null=True) # 공간 사용 범위
    # facility = ArrayField(models.CharField(max_length=20), blank=True, null=True, default=list)  # 시설 정보 # PostgreSQL
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "board"

    # def __str__(self):
    #     Board.objects.filter(date__lte=timezone.now())\
    #                 .order_by('created_at')
    #     return self.title

class Address(models.Model):
    postCode = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    latitude = models.CharField(max_length=50)
    longitude = models.CharField(max_length=50)
    kakaoLatitude = models.CharField(max_length=50)
    kakaoLongitude = models.CharField(max_length=50)

    class Meta:
        db_table = "addresses"