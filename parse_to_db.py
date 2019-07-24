import random
import time
from csv import DictWriter
from requests_html import HTMLSession
from sqlite3 import *

SESSION = HTMLSession()


def parser_links_from_category_page():
    category_base_url = 'https://www.olx.ua/zhivotnye/sobaki/'
    response = SESSION.get(category_base_url)
    category_base_inner_urls_xpath = response.html.xpath("//div/h3/a/@href")
    urls_list = []

    for i in category_base_inner_urls_xpath:
        urls_list.append(i)

    return urls_list

def get_information_from_urls():
    urls_to_get_info = parser_links_from_category_page()
    text_xpath = '//div/h3/a/strong/text()'
    price_xpath = '//div//p[@class="price"]/strong/text()'
    city_xpath = '//div//small[@class="breadcrumb x-normal"][1]/span'

    for link in urls_to_get_info:
        response = SESSION.get(link)
        time.sleep(random.randint(1, 5))
        print(response)


get_information_from_urls()


    # for url in category_urls:
    #     response = None
    #     prox = None
    #
    #     for _ in range(5):
    #         prox = random.choice(proxies_list)
    #         proxies = {'http': prox, 'https': prox}
    #         headers = {'User-Agent': random.choice(user_agents)}
    #         try:
    #             response = SESSION.get(url, proxies=proxies, headers=headers, timeout=4)
    #             if response.status_code == 200:
    #                 break
    #             else:
    #                 response = None
    #         except Exception as e:
    #             print(e, type(e))
    #             response = None
    #
    #     if not response:
    #         print('За 5 попыток ответ не пришел')
    #         continue
    #
    #     print('Запрос обработан верно. Прокси:', prox)
    #
    #     links_xpath = '//div/h3/a/@href'
    #     text_xpath = '//div/h3/a/strong/text()'
    #     price_xpath = '//div//p[@class="price"]/strong/text()'
    #     city_xpath = '//div//small[@class="breadcrumb x-normal"][1]/span'
    #     time_xpath = '//div//small[@class="breadcrumb x-normal"][2]/span'
    #
    #     ad_links_list = response.html.xpath(links_xpath)
    #     name_list = response.html.xpath(text_xpath)
    #     price_list = response.html.xpath(price_xpath)
    #     city_list = response.html.xpath(city_xpath)
    #     time_list = response.html.xpath(time_xpath)
    #
    #     price_list_fixed = []
    #     for price in price_list:
    #         try:
    #             fixed_pr = float(price.replace(' грн.', '').replace(' ', ''))
    #         except Exception as e:
    #             print(e)
    #             fixed_pr = '---'
    #         price_list_fixed.append(fixed_pr)
    #
    #     city_list = [elem.text for elem in city_list]
    #     time_list = [elem.text for elem in time_list]
    #
    #     for i in range(len(ad_links_list)):
    #
    #         ad = {
    #             'name': name_list[i],
    #             'link': ad_links_list[i],
    #             'price': price_list_fixed[i],
    #             'city': city_list[i],
    #             'time': time_list[i],
    #             'more_info': parser_item(ad_links_list[i])
    #         }
    #
    #         result.append(ad)
    #
    # return result