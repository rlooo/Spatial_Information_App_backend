import operator

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404

import json

from django.views import View
from openpyxl import load_workbook
from rest_framework.generics import ListAPIView

from board.models import PutOut, LookFor, ApplySpace, BldRgstService, QnA, Notice, BuildingImage
from board.serializer import PutOutListSerializer, NoticeListSerializer, QnAListSerializer

import requests

import PublicDataReader as pdr

from django.views.generic.detail import SingleObjectMixin
from django.http import FileResponse
from django.core.files.storage import FileSystemStorage


from user.models import Account
#새로운 공간내놓기 게시물 작성하는 함수2
def new_putout2(request):
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
        facilities = request.POST.get('facilities')
        remarks = request.POST.get('remarks')

        address = request.POST.get('address')
        detailAddress = request.POST.get('detailAddress')
        kakaoLatitude = request.POST.get('kakaoLatitude')
        kakaoLongitude = request.POST.get('kakaoLongitude')

        # 도로명 주소를 지번 주소로 변환해서 건축물 대장 불러오기
        bldInfo = openAPIData(address)

        facilities = facilities.replace('[','').replace(']','')
        facilities = facilities.split(',')
        facilities = [int(i) for i in facilities]

        if Account.objects.filter(uid=uid).exists():
            user = Account.objects.get(uid=uid)

            new_article = PutOut.objects.create(
                author=user,
                bldInfo=bldInfo,
                name=name,
                contact=contact,
                address=address,
                kakaoLatitude=kakaoLatitude,
                kakaoLongitude=kakaoLongitude,
                area=int(area),
                floor=int(floor),
                deposit=int(deposit),
                price=int(price),
                discussion=int(discussion),
                client=int(client),
                sort=int(sort),
                count=int(count),
                range=int(range),
                facility=facilities,
                detailAddress=detailAddress,
                remarks=remarks,
            )

            # 이미지 파일 저장
            image_set = request.FILES.getlist('file')
            for image_data in image_set:
                image = BuildingImage.objects.create(putout=new_article, image=image_data)
                image.save()

                new_article.thumbnail = image.image.url

            new_article.save()

            return HttpResponse(status=200)
        return HttpResponse(status=401) # 클라이언트가 권한이 없을 때


#새로운 공간구하기 게시물 작성하는 함수
def new_lookfor(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        business = request.POST.get('business')
        area = request.POST.get('area')
        deposit = request.POST.get('deposit')
        price = request.POST.get('price')
        discussion = request.POST.get('discussion')


        if Account.objects.filter(uid=uid).exists():
            user = Account.objects.get(uid=uid)

            new_article = LookFor.objects.create(
                author=user,
                name=name,
                contact=contact,
                business=business,
                area=int(area),
                deposit=int(deposit),
                price=int(price),
                discussion=int(discussion),
            )

            new_article.save()

            return HttpResponse(status=200)

# 공간 신청하기
def applySpace(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        name = request.POST.get('name')
        contact = request.POST.get('contact')
        business = request.POST.get('business')
        deposit = request.POST.get('deposit')
        price = request.POST.get('price')
        discussion = request.POST.get('discussion')
        building_id = request.POST.get('buildingId')


        if Account.objects.filter(uid=uid).exists():
            user = Account.objects.get(uid=uid)

            if PutOut.objects.filter(id=building_id).exists():
                building = PutOut.objects.get(id=building_id)

            applySpace = ApplySpace.objects.create(
                author=user,
                building=building,
                name=name,
                contact=contact,
                business=business,
                deposit=int(deposit),
                price=int(price),
                discussion=int(discussion),
            )

            applySpace.save()

            return HttpResponse(status=200)

# 게시글 삭제 기능
def putout_delete(request, pk):
    putout = get_object_or_404(PutOut, id=pk)
    putout.delete()
    return HttpResponse(status=200)

# 게시물 상세 조회하는 함수
def putout_detail(request, pk):
    # 게시글(Post) 중 pk(primary_key)를 이용해 하나의 게시글(post)를 검색
    board = PutOut.objects.get(id=pk)

    if BuildingImage.objects.filter(putout=board).exists():
        imgList = []
        objects = BuildingImage.objects.filter(putout=board)
        for _object in objects:
            imgList.append(_object.image.url)

    return JsonResponse({
        'id': board.id,
        'name': board.name,
        'contact': board.contact,
        'address':board.address,
        'detail_address':board.detailAddress,
        'kakaoLatitude':board.kakaoLatitude,
        'kakaoLongitude': board.kakaoLongitude,
        'area':board.area,
        'floor':board.floor,
        'deposit':board.deposit,
        'price':board.price,
        'discussion':board.get_discussion_display(),
        'client':board.get_client_display(),
        'sort':board.get_sort_display(),
        'count':board.get_count_display(),
        'range':board.get_range_display(),
        'imgList': imgList,
        'thumbnail': imgList[0],
        'facility':board.get_facility_display(),
        'created_at':board.created_at,

        'platArea': board.bldInfo.platArea,  # 대지면적
        'archArea': board.bldInfo.archArea, # 건축면적
        'bcRat': board.bldInfo.bcRat,   # 건폐울
        'vlRat': board.bldInfo.vlRat,   # 용적률
        'grndFlrCnt': board.bldInfo.grndFlrCnt, # 지상층수
        'ugrndFlrCnt': board.bldInfo.ugrndFlrCnt,   # 지하층수
        'mainPurpsCdNm': board.bldInfo.mainPurpsCdNm,   # 주용도
        'etcPurps': board.bldInfo.etcPurps, # 기타용도
        'strctCdNm': board.bldInfo.strctCdNm,   # 구조
        'totPkngCnt': board.bldInfo.totPkngCnt, # 총주차수
    }, json_dumps_params={'ensure_ascii': False}, status=200)


# 모든 '공간 구하기' 게시글들을 불러오기
class PutOutListView(ListAPIView):
    queryset = PutOut.objects.all()
    serializer_class = PutOutListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)


def convertPNU(request):
    # 도로명 주소를 지번주소로 변환
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={}'.format("서울 동대문구 홍릉로17길 36")
    headers = {"Authorization": "KakaoAK 7f44810be24159eb8b2748926096d3d8"}
    place = requests.get(url, headers=headers).json()['documents']

    print(place[0].get('address').get('address_name'))
    address_name = place[0].get('address').get('address_name') # 지번주소 서울 동대문구 제기동 289-15

    address = address_name.split()
    print(address)

    sido = address[0]
    sigungu = address[1]
    dong = address[2]
    daesi = str(1) # 필지구분(일반:1)
    bun = address[3].split('-')[0].zfill(4) # 본번
    ji = address[3].split('-')[1].zfill(4) # 부번

    print(sido)
    print(sigungu)
    print(dong)
    print(daesi)
    print(bun)
    print(ji)

    rb = load_workbook("C:/Users/USER/Desktop/공간정보기반앱/KIKcd_B.20181210.xlsx") # 엑셀파일
    sheet = rb['KIKcd_B'] # 시트

    for i in sheet.rows:
        if(operator.eq(i[3].value, dong)):
            print(i[0].value)
            code = i[0].value # 법정동 코드

    PNU = code+daesi+bun+ji
    print(PNU)

def openAPIData(addr):
    print(pdr.__version__)
    serviceKey = "KYOIVq7wl4Potw9VACNS429a%2FnGO%2BxzFFa%2BXyKs5I6YNm85eUF4N9AjAhf7tp1wVx0bvB6axbFPyBKUJUo4mfw%3D%3D"

    # 3. 국토교통부 건축물대장정보 서비스 OpenAPI 세션 정의하기
    # debug: True이면 모든 메시지 출력, False이면 오류 메시지만 출력 (기본값: False)
    bd = pdr.Building(serviceKey, debug=True)

    # 도로명 주소를 지번주소로 변환
    url = 'https://dapi.kakao.com/v2/local/search/address.json?query={}'.format(addr) # 수정할 것
    headers = {"Authorization": "KakaoAK 7f44810be24159eb8b2748926096d3d8"}
    place = requests.get(url, headers=headers).json()['documents']

    print(place[0].get('address').get('address_name'))
    address_name = place[0].get('address').get('address_name')  # 지번주소 서울 동대문구 제기동 289-15
    # address_name = '서울 동대문구 제기동 289-15'
    address = address_name.split()
    print(address)

    sigungu = address[1]
    dong = address[2]
    daesi = str(1)  # 필지구분(일반:1)

    bun = address[3].split('-')[0].zfill(4)  # 본번
    try:
        ji = address[3].split('-')[1].zfill(4)  # 부번
    except IndexError as e:
        ji = "0000"
        print(e)

    print(bun)
    print(ji)
    # 4. 지역코드(시군구코드) 검색하기
    # code = pdr.code_list()
    code = pdr.code_bdong()
    print(code.loc[(code['시군구명'].str.contains(sigungu, na=False)) & (code['읍면동명'].str.contains(dong, na=False))])
    result = code.loc[(code['시군구명'].str.contains(sigungu, na=False)) & (code['읍면동명'].str.contains(dong, na=False))]
    sigunguCd = str(result['시군구코드'].values[0])
    dongCd = str(result['법정동코드'].values[0])[5:]
    print(sigunguCd) # 시군구코드(5)
    print(dongCd) # 읍면동코드(5)

    # 5. 건축물대장정보 오퍼레이션별 데이터 조회
    # category = "총괄표제부"  # 건축물대장 종류 (ex. 표제부, 총괄표제부, 전유부 등)
    #
    # df = bd.read_data(category=category, sigunguCd=sigunguCd, bjdongCd=dongCd, bun=bun, ji=ji)
    # df.head()
    # print(df.head())

    category2 = "표제부"  # 건축물대장 종류

    df2 = bd.read_data(category=category2, sigunguCd=sigunguCd, bjdongCd=dongCd, bun=bun, ji=ji)
    print(df2.head())

    try:
        bldInfo = BldRgstService.objects.create(
            platArea=df2['대지면적'].values[0],  # 대지면적
            archArea=df2['건축면적'].values[0],  # 건축면적
            bcRat=df2['건폐율'].values[0],  # 건폐울
            vlRat=df2['용적률'].values[0],  # 용적률
            grndFlrCnt=df2['지상층수'].values[0],  # 지상층수
            ugrndFlrCnt=df2['지하층수'].values[0],  # 지하층수
            mainPurpsCdNm=df2['주용도코드명'].values[0],  # 주용도
            etcPurps=df2['기타용도'].values[0],  # 기타용도
            strctCdNm=df2['구조코드명'].values[0],  # 구조
            totPkngCnt=(df2['옥내기계식대수'].values[0] + df2['옥외기계식대수'].values[0] + df2['옥내자주식대수'].values[0] + df2['옥외자주식대수'].values[0])   # 총주차수
        )
    except AttributeError as e:
        bldInfo = BldRgstService.objects.create(
            platArea = None,  # 대지면적
            archArea = None,  # 건축면적
            bcRat = None,  # 건폐울
            vlRat = None,  # 용적률
            grndFlrCnt = None,  # 지상층수
            ugrndFlrCnt = None,  # 지하층수
            mainPurpsCdNm = None,  # 주용도
            etcPurps = None,  # 기타용도
            strctCdNm = None,  # 구조
            totPkngCnt = None  # 총주차수
        )
        print(e)
    finally:
        bldInfo.save()
        return bldInfo

#새로운 QnA 게시물 작성하는 함수
def new_qna(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        title = request.POST.get('title')
        content = request.POST.get('content')

        if Account.objects.filter(uid=uid).exists():
            user = Account.objects.get(uid=uid)

        new_article = QnA.objects.create(
            author=user,
            title=title,
            content=content,
        )

        new_article.save()

        return HttpResponse(status=200)


# 모든 공지사항 게시글들을 불러오기
class NoticeListView(ListAPIView):
    queryset = Notice.objects.all()
    serializer_class = NoticeListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)


# 모든 Q&A 게시글들을 불러오기
class QnAListView(ListAPIView):
    queryset = QnA.objects.all()
    serializer_class = QnAListSerializer

    def list(self, request):
        queryset = self.get_queryset()
        serializer_class = self.get_serializer_class()
        serializer = serializer_class(queryset, many=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        return HttpResponse(json.dumps(serializer.data, ensure_ascii=False, indent='\t'), status=200)

# 이미지 보내기
class ImageDownloadView(SingleObjectMixin, View):
    def get(self, request, putout_id):
        putout_object = PutOut.objects.get(id=putout_id)
        object = BuildingImage.objects.get(putout=putout_object)
        file_path = object.attached.path
        print(file_path)
        file_type = object.content_type
        fs = FileSystemStorage(file_path)
        response = FileResponse(fs.open(file_path, 'rb'), content_type=file_type)
        response['Content-Disposition'] = f'attachment; filename={object.get_filename()}'

        return response


# # 게시글 수정 기능
# def putout_modify(request, pk):
#     board = get_object_or_404(Board, id=pk)
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



# def openAPIData2(request):
#     serviceKey = "KYOIVq7wl4Potw9VACNS429a%2FnGO%2BxzFFa%2BXyKs5I6YNm85eUF4N9AjAhf7tp1wVx0bvB6axbFPyBKUJUo4mfw%3D%3D"
#
#     url = 'http://apis.data.go.kr/1611000/nsdi/GisBuildingService/wfs/getGisGnrlBuildingWFS'
#     params = {'serviceKey': 'KYOIVq7wl4Potw9VACNS429a/nGO+xzFFa+XyKs5I6YNm85eUF4N9AjAhf7tp1wVx0bvB6axbFPyBKUJUo4mfw==', 'typename': 'F171', 'bbox': '197977.042,451073.098,198432.41,451515.861,EPSG:5174',
#               'pnu': '1114011400102500000', 'maxFeatures': '10', 'resultType': 'results', 'srsName': 'EPSG:5174'}
#
#
#     response = requests.get(url, params=params)
#     print(response.content)
#
#     data = response.text
#     print(data)
#     soup = BeautifulSoup(data, 'html.parser')
#     print(soup)
#     print(soup.find('nsdi:buld_plot_ar').text)
#
#     db = GisBuildingService(BULD_PLOT_AR=soup.find('nsdi:buld_plot_ar').text,
#                                 BULD_BILDNG_AR=soup.find('nsdi:buld_bildng_ar').text,
#                                 MEASRMT_RT=soup.find('nsdi:measrmt_rt').text, BTL_RT=soup.find('nsdi:btl_rt').text,
#                                 STRCT_CODE=soup.find('nsdi:strct_code').text,
#                                 MAIN_PRPOS_CODE=soup.find('nsdi:main_prpos_code').text,
#                                 GROUND_FLOOR_CO=soup.find('nsdi:ground_floor_co').text,
#                                 UNDGRND_FLOOR_CO=soup.find('nsdi:undgrnd_floor_co').text,
#                                 TOT_PARKNG_CO=soup.find('nsdi:tot_parkng_co').text)
#     db.save()
#     return HttpResponse(status=200)