import re
from decimal import Decimal
from selenium import webdriver

__all__ = (
    'TravelData',
)


class TravelData:
    city = "Amsterdam"
    country = "Netherlands"

    def __init__(self, product_id):
        self.product_id = product_id
        self.product_image_url = None
        self.product_profile_name = None
        self.product_name = None
        self.price = None
        self.category = None
        self.time = None

    # def get_travel_detail_url(self,id):
    #     url = "https://www.myrealtrip.com/offers/" + id
    #     return url

    def travel_infomation(self, country, city):
        result = []
        driver = webdriver.Chrome('chromedriver')
        main_url = "https://www.myrealtrip.com/offers?" + "city=" + city + "&country=" + country
        driver.get(main_url)
        travel_product_list = driver.find_element_by_class_name('list-wrapper').find_elements_by_class_name('item')

        for product in travel_product_list:
            product_id_string = product.find_element_by_class_name('offer-link').get_attribute("href")
            product_id = re.sub(r'[^\d]', '', product_id_string)
            product_image_url = product.find_element_by_class_name('profile-img').get_attribute("src")
            product_profile_name = product.find_element_by_class_name('profile-name').text
            product_name = product.find_element_by_class_name('name').text
            price = product.find_element_by_class_name('price').get_attribute("data-offer-price")
            category = product.find_element_by_class_name('category').text
            time = product.find_element_by_class_name('meta-infos').text

            # self.product_id=product_id
            # self.product_image_url=product_image_url
            # self.product_profile_name=product_profile_name
            # self.product_name=product_name
            # self.price=price
            # self.category=category
            # self.time=time
            result.append({
                'product_id': product_id,
                'product_image_url': product_image_url,
                'product_profile_name': product_profile_name,
                'product_name': product_name,
                'price': re.sub(r'[^\d.]', '', price),
                'category': category,
                'time': time,
            })

        print(result)
        return result

# travel_products = travel_infomation('Netherlands', 'Amsterdam')
