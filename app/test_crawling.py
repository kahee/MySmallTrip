import requests
from bs4 import BeautifulSoup


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
        # print(img_photos)

        photos = [item.find('source').get('srcset') for item in img_photos]
        print(photos)
        result.append(photos)

        # 상품 소개

        introduce_title = soup.find('div', class_='introduce-container').find('div', class_='title').get_text(
            strip=True)
        introduce_content = soup.find('div', class_='introduce-container').find('p', class_='more').get_text(strip=True)
        introduce = dict()
        introduce[introduce_title] = introduce_content
        print(introduce)
        result.append(introduce)
        return result


if __name__ == '__main__':

    crawler = TravelData()
    crawler.travel_detail('2122')