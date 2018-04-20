import magic
from django.db import models

from travel.models import CityInformation, CompanyInformation
from .product_base import ProductBase
from io import BytesIO
from PIL import Image
from django.core.files import File

__all__ = (
    'TravelInformation',
)


class TravelInformation(ProductBase):
    CATEGORY_TYPE_Ticket = 'ticket'
    CATEGORY_TYPE_Convenience = 'convenience'
    CATEGORY_TYPE_GuideTour = 'guide_tour'
    CATEGORY_TYPE_Restaurant = 'restaurant'
    CATEGORY_TYPE_Activity = 'activity'
    CATEGORY_TYPE_Accommodation = 'accomodation'
    CATEGORY_TYPE_Enjoy = 'enjoy'

    CHOICES_CATEGORY_TYPE = (
        (CATEGORY_TYPE_Ticket, '교통/티켓'),
        (CATEGORY_TYPE_Convenience, '여행편의'),
        (CATEGORY_TYPE_GuideTour, '가이드투어'),
        (CATEGORY_TYPE_Restaurant, '식당'),
        (CATEGORY_TYPE_Activity, '액티비티'),
        (CATEGORY_TYPE_Accommodation, '숙박/민박'),
        (CATEGORY_TYPE_Enjoy, '즐길거리')
    )

    travel_id = models.IntegerField('ID')

    name = models.CharField('상품명', max_length=200)
    category = models.CharField('카테고리', max_length=40, choices=CHOICES_CATEGORY_TYPE, blank=True)

    theme = models.CharField('테마', max_length=100, blank=True)
    # producttype 예시) 상품유형: 상품유형
    product_type = models.CharField('상품타입', max_length=100, blank=True)

    language = models.CharField('언어', max_length=40)
    city = models.ForeignKey(
        CityInformation,
        on_delete=models.CASCADE,
        verbose_name='city')
    time = models.CharField('소요시간', max_length=40)
    company = models.ForeignKey(
        CompanyInformation,
        on_delete=models.CASCADE,
        verbose_name='company')

    description_title = models.TextField('상품설명제목', blank=True, null=True)
    description = models.TextField('상품설명', blank=True)
    meeting_time = models.CharField('만남시간', max_length=100, blank=True)
    meeting_place = models.CharField('만남장소', max_length=100, blank=True)

    price = models.IntegerField('상품금액', default=0)
    price_descrption = models.TextField('상품금액 포함사항', blank=True)

    max_people = models.IntegerField('최대 사람 수', default=0)

    main_image = models.ImageField('대표이미지', upload_to='main_image')
    main_image_thumbnail= models.ImageField(upload_to='main-image-thumbnail')

    def save(self, *args, **kwargs):
        self._save_thumbnail_process()
        super().save(*args, **kwargs)

    def _save_thumbnail_process(self):
        """
        save() 메서드 실행 도중 img_profile필드의 썸네일 생성에 관한 로직
        :return:
        """
        if self.main_image:
            # 이미지파일의 이름과 확장자를 가져옴
            full_name = self.main_image.name.rsplit('/')[-1]
            full_name_split = full_name.rsplit('.', maxsplit=1)

            temp_file = BytesIO()
            temp_file.write(self.main_image.read())
            temp_file.seek(0)
            mime_info = magic.from_buffer(temp_file.read(), mime=True)
            temp_file.seek(0)

            name = full_name_split[0]
            ext = mime_info.split('/')[-1]

            # Pillow를 사용해 이미지 파일 로드
            im = Image.open(self.main_image)
            # 썸네일 형태로 데이터 변경
            im.thumbnail((375, 199))

            # 썸네일 이미지 데이터를 가지고 있을 임시 메모리 파일 생성
            temp_file = BytesIO()
            # 임시 메모리 파일에 Pillow인스턴스의 내용을 기록
            im.save(temp_file, ext)
            # 임시 메모리파일을 Django의 File로 한번 감싸 썸네일 필드에 저장
            self.main_image_thumbnail.save(f'{name}_thumbnail.{ext}', File(temp_file), save=False)
        else:
            self.main_image_thumbnail.delete(save=False)

    def __str__(self):
        return self.name
