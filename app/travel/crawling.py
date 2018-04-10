import re
from datetime import datetime
import time

import os
import requests
from bs4 import BeautifulSoup
from io import BytesIO

from django.core.files import File
from selenium import webdriver

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')
import django

django.setup()
from travel.models import CityInformation, CompanyInformation, TravelInformationImage, TravelSchedule

from utils.file import get_buffer_ext

__all__ = (
    'TravelData',
)


class TravelData:

    def travel_detail(self, keyword, ):
        url = "https://www.myrealtrip.com/offers/" + keyword
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        result = []

        # 상품유형, 만나는시간, 소유시간, 언어 정보
        products_type = soup.find('div', class_='info-icon-container').find_all('div', class_='text-sm')
        products_info = soup.find('div', class_='info-icon-container').find_all('div', class_='text-bold')
        type = [item.get_text(strip=True) for item in products_type]
        info = [item.get_text(strip=True) for item in products_info]

        product_info = dict(zip(type, info))
        # print(product_info)
        result.append(product_info)

        # 가이드 정보
        guide_page = soup.find('div', class_='guide-container')
        guide_img_profile = guide_page.find('img', class_='img-profile').get('src')
        guide_name = guide_page.find('div', class_='guide-name').get_text(strip=True)
        guide_description = guide_page.find('div', class_='guide-description').get_text(strip=True)
        guide = dict()
        guide['img_profile'] = guide_img_profile
        guide['name'] = guide_name
        guide['description'] = guide_description
        # print(guide)
        result.append(guide)
        # 사진
        img_photos = soup.find('ul', class_='item-container').find_all('picture')
        photos = [item.find('source').get('srcset') for item in img_photos]
        print(photos)
        result.append(photos)

        # 상품 소개

        introduce_title = soup.find('div', class_='introduce-container').find('div', class_='title').get_text(
            strip=True)
        introduce_content = soup.find('div', class_='introduce-container').find('p', class_='more').get_text(strip=True)
        introduce = dict()
        introduce[introduce_title] = introduce_content
        # print(introduce)
        result.append(introduce)
        return result

    def travel_infomation(self, country, city):
        result = []
        driver = webdriver.Chrome('chromedriver')
        main_url = "https://www.myrealtrip.com/offers?" + "city=" + city + "&country=" + country
        driver.get(main_url)
        travel_product_list = driver.find_element_by_class_name('list-wrapper').find_elements_by_class_name('item')
        # product = driver.find_element_by_class_name('list-wrapper').find_element_by_class_name('item')
        for product in travel_product_list:
            product_id_string = product.find_element_by_class_name('offer-link').get_attribute("href")
            product_id = re.sub(r'[^\d]', '', product_id_string)
            print(product_id)
            # product_image_url = product.find_element_by_class_name('profile-img').get_attribute("src")
            product_profile_name = product.find_element_by_class_name('profile-name').text
            product_name = product.find_element_by_class_name('name').text
            price = product.find_element_by_class_name('price').get_attribute("data-offer-price")
            category = product.find_element_by_class_name('category').text
            time = product.find_element_by_class_name('meta-infos').text

            # detail_info = self.travel_detail('1474')
            detail_info = self.travel_detail(product_id)
            detail_basic_info = detail_info[0]

            if '상품 유형' in detail_basic_info:
                product_type = detail_basic_info['상품 유형']
            else:
                product_type = ''

            if '만나는 시간' in detail_basic_info:
                meeting_time = detail_basic_info['만나는 시간']
            else:
                meeting_time = ''
            # if detail_basic_info['소요 시간']:
            #     time = detail_basic_info['소요 시간']
            if '언어' in detail_basic_info:
                language = detail_basic_info['언어']
            else:
                language = ''
            detail_second_info = detail_info[1]

            if 'img_profile' in detail_second_info:
                guide_img_profile = detail_second_info['img_profile']
            else:
                guide_img_profile = ''

            if 'name' in detail_second_info:
                guide_name = detail_second_info['name']
            else:
                guide_name = ''
            if 'description' in detail_second_info:
                guide_description = detail_second_info['description']
            else:
                guide_description = ''
            detail_third_info = detail_info[2]

            if detail_third_info:
                product_image = detail_third_info
            else:
                product_image = ''

            detail_fourth_info = detail_info[3]
            if detail_fourth_info:
                product_description = detail_fourth_info
            else:
                product_description = ''

            result.append({
                'product_id': product_id,
                # 'product_image_url': product_image_url,
                'product_profile_name': product_profile_name,
                'product_name': product_name,
                'price': re.sub(r'[^\d.]', '', price),
                'category': category,
                'time': time,
                'product_type': product_type,
                'meeting_time': meeting_time,
                'language': language,
                'city': city,
                'guide_img_profile': guide_img_profile,
                'guide_name': guide_name,
                'guide_description': guide_description,
                'product_image': product_image,
                'product_description': product_description,

            })
        return result


if __name__ == '__main__':
    from travel.models import TravelInformation

    crawler = TravelData()
    travel_infos = crawler.travel_infomation('Netherlands', 'Amsterdam')

    for travel_info in travel_infos:

        # 도시, 회사정보 저장
        city, _ = CityInformation.objects.get_or_create(
            name=travel_info['city'],
            continent='Europe',
            nationality=travel_info['city'],
        )

        company, _ = CompanyInformation.objects.get_or_create(
            name=travel_info['guide_name'],
            info=travel_info['guide_description'],
        )
        print(city, company)

        # 상품정보 저장

        travel, _ = TravelInformation.objects.get_or_create(
            travel_id=travel_info['product_id'],
            name=travel_info['product_name'],
            category=travel_info['category'],
            theme='',
            product_type=travel_info['product_type'],
            language=travel_info['language'],
            city=city,
            time=travel_info['time'],
            company=company,
            description=travel_info['product_description'],
            meeting_time=travel_info['meeting_time'],
            meeting_place='where',
            price=travel_info['price'],
            # is_usable=True,
        )

        # 상품이미지 저장 부분

        id = travel_info['product_id']
        images = travel_info['product_image']

        for image in images:
            url_img_product = requests.get(image)
            # print(url_img_product.content)
            binary_data = url_img_product.content
            temp_file = BytesIO()
            temp_file.write(binary_data)
            temp_file.seek(0)
            # temp_file = download(url_img_product)
            file_name = '{product_id}.{img}.{ext}'.format(
                product_id=id,
                img=datetime.now(),
                ext=get_buffer_ext(temp_file),
            )
            timestamp = int(time.mktime(datetime.now().timetuple()))
            time.sleep(0.5)

            image, _ = TravelInformationImage.objects.get_or_create(
                travel_id=travel,
                image_id=timestamp,
            )

            if image in TravelInformation.objects.all():
                image.product_image.delete()
            image.product_image.save(file_name, File(temp_file))

        print(travel)
