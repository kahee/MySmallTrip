import magic
from django.core.files import File
from django.db import models
from io import BytesIO
from PIL import Image

from .product_base import ProductBase
from .travel_information import TravelInformation


class TravelInformationImage(ProductBase):
    travel_id = models.ForeignKey(
        TravelInformation,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image_id = models.IntegerField(
        '이미지 ID'
    )
    product_image = models.ImageField('상품이미지', upload_to='product')
    product_image_thumbnail = models.ImageField(upload_to='product-thumbnail')

    def save(self, *args, **kwargs):
        self._save_thumbnail_process()
        super().save(*args, **kwargs)

    def _save_thumbnail_process(self):
        """
        save() 메서드 실행 도중 img_profile필드의 썸네일 생성에 관한 로직
        :return:
        """
        if self.product_image:
            # 이미지파일의 이름과 확장자를 가져옴
            full_name = self.product_image.name.rsplit('/')[-1]
            full_name_split = full_name.rsplit('.', maxsplit=1)

            temp_file = BytesIO()
            temp_file.write(self.product_image.read())
            temp_file.seek(0)
            mime_info = magic.from_buffer(temp_file.read(), mime=True)
            temp_file.seek(0)

            name = full_name_split[0]
            ext = mime_info.split('/')[-1]

            # Pillow를 사용해 이미지 파일 로드
            im = Image.open(self.product_image)
            # 썸네일 형태로 데이터 변경
            im.thumbnail((375, 199))

            # 썸네일 이미지 데이터를 가지고 있을 임시 메모리 파일 생성
            temp_file = BytesIO()
            # 임시 메모리 파일에 Pillow인스턴스의 내용을 기록
            im.save(temp_file, ext)
            # 임시 메모리파일을 Django의 File로 한번 감싸 썸네일 필드에 저장
            self.product_image_thumbnail.save(f'{name}_thumbnail.{ext}', File(temp_file), save=False)
        else:
            self.product_image_thumbnail.delete(save=False)