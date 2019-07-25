from parse_to_db_2_initialization import AdvNum, AdvTitlePrice
from parse_to_db import parser_links_from_category_page
from requests_html import HTMLSession
import re
import random
import time

SESSION = HTMLSession()


def add_info_to_the_tables():
    pages_with_advs = parser_links_from_category_page()
    clean_text = str

    for adv_urls in pages_with_advs:
        response_new = SESSION.get(adv_urls)
        number_of_adv = response_new.html.xpath('//em/small/text()')
        text_xpath = response_new.html.xpath('//div[@class="offer-titlebox"]/h1/text()')
        price_xpath = response_new.html.xpath('//div[@class="price-label"]/strong/text()')

        for text in text_xpath:
            clean_text = text.strip()

        AdvNum.create(adv_url=re.sub('[\'\[\]]', '', str(number_of_adv)))
        AdvTitlePrice.create(title=clean_text, price=re.sub('[\'\.\[\]]', '', str(price_xpath)))
        time.sleep(random.randint(1, 3))


if __name__ == "__main__":
    add_info_to_the_tables()
