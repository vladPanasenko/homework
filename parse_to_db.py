import random
import time
from requests_html import HTMLSession
import re
import sqlite3

SESSION = HTMLSession()
conn = sqlite3.connect('hw_part_1.db')


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

    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS urls_data
                 (text_from_url text, price text)''')

    clean_text = str

    for link in urls_to_get_info:
        response = SESSION.get(link)
        text_xpath = response.html.xpath('//div[@class="offer-titlebox"]/h1/text()')
        price_xpath = response.html.xpath('//div[@class="price-label"]/strong/text()')

        for text in text_xpath:
            clean_text = text.strip()

        c.execute("INSERT INTO urls_data VALUES (?, ?);", (clean_text, (re.sub('[\'\.\[\]]', '', str(price_xpath)))))
        conn.commit()
        time.sleep(random.randint(1, 5))

    c.close()
    conn.close()


if __name__ == "__main__":
    get_information_from_urls()
