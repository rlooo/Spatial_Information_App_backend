from django.db import models

# Create your models here.
from django.utils import timezone
from multiselectfield import MultiSelectField

from user.models import Account

class BldRgstService(models.Model):
    platArea = models.FloatField(null=True)  # 대지면적
    archArea = models.FloatField(null=True)  # 건축면적
    bcRat = models.FloatField(null=True) # 건폐울
    vlRat = models.FloatField(null=True) # 용적률
    grndFlrCnt = models.IntegerField(null=True)  # 지상층수
    ugrndFlrCnt = models.IntegerField(null=True) # 지하층수
    mainPurpsCdNm = models.CharField(max_length=100,null=True)  # 주용도
    etcPurps = models.CharField(max_length=500, null=True) # 기타용도
    strctCdNm = models.CharField(max_length=50,null=True) # 구조
    totPkngCnt = models.IntegerField(null=True)   # 총주차수

class PutOut(models.Model):
    DISCUSSION_CHOICES = [
        (1, '보증금 / 월세 협의 불가능'),
        (2, '보증금 / 월세 협의 가능'),
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
    bldInfo = models.ForeignKey(BldRgstService, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    address = models.CharField(max_length=50, null=True) # 도로명 주소
    detailAddress = models.CharField(max_length=50) # 상세주소
    kakaoLatitude = models.CharField(max_length=50, null=True, blank=True)
    kakaoLongitude = models.CharField(max_length=50, null=True, blank=True)
    area = models.IntegerField()
    floor = models.IntegerField()
    deposit = models.IntegerField() # 보증금
    price = models.IntegerField() # 월세
    discussion = models.PositiveSmallIntegerField(choices=DISCUSSION_CHOICES, null=True)  # 협의 가능 여부
    client = models.PositiveSmallIntegerField(choices=CLIENT_CHOICES, null=True)  # 의뢰인
    sort = models.PositiveSmallIntegerField(choices=SORT_CHOICES, null=True)  # 거래 종류
    count = models.PositiveSmallIntegerField(choices=COUNT_CHOICES, null=True)  # 공간 개수
    range = models.PositiveSmallIntegerField(choices=RANGE_CHOICES, null=True)  # 공간 사용 범위
    facility = MultiSelectField(choices=FACILITY_CHOICES, null=True)  # 시설 정보
    remarks = models.TextField(null=True, blank=True) # 비고란
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "putout"
        verbose_name_plural = "공간 나누기"

    def __str__(self):
        return f' {self.address} [{self.name}]'

class BuildingImage(models.Model):
    putout = models.ForeignKey(PutOut, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='putout', blank=True, null=True)


class LookFor(models.Model):
    DISCUSSION_CHOICES = [
        (1, '보증금 / 월세 협의 불가능'),
        (2, '보증금 / 월세 협의 가능'),
    ]

    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    business = models.CharField(max_length=50)
    area = models.IntegerField()
    deposit = models.IntegerField()
    price = models.IntegerField()
    discussion = models.PositiveSmallIntegerField(choices=DISCUSSION_CHOICES, null=True)  # 협의 가능 여부
    remarks = models.TextField(null=True, blank=True)  # 비고란
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "lookfor"
        verbose_name_plural = "공간 구하기"

    def __str__(self):
        return f' 신청인: {self.name} '


class ApplySpace(models.Model):
    DISCUSSION_CHOICES = [
        (1, '보증금 / 월세 협의 불가능'),
        (2, '보증금 / 월세 협의 가능'),
    ]

    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    building = models.ForeignKey(PutOut, on_delete=models.CASCADE, blank=True, null=True)
    name = models.CharField(max_length=50)
    contact = models.CharField(max_length=50)
    business = models.CharField(max_length=50)
    deposit = models.IntegerField()
    price = models.IntegerField()
    discussion = models.PositiveSmallIntegerField(choices=DISCUSSION_CHOICES, null=True)  # 협의 가능 여부
    remarks = models.TextField(null=True, blank=True)  # 비고란
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f'{self.building} '

    class Meta:
        db_table = "applySpace"
        verbose_name_plural = "공간 신청하기"

class QnA(models.Model):
    author = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=50)
    content = models.TextField()
    answer = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} '

    class Meta:
        db_table = "qna"
        verbose_name_plural = "Q&A"

class Notice(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    link = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title} '

    class Meta:
        db_table = "notice"
        verbose_name_plural = "공지사항"






