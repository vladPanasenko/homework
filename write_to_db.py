import random
import datetime
from pprint import pprint
from time import sleep
from requests_html import HTMLSession
from create_db import Top
from queue import Queue
from threading import Thread


COUNT = 100
DOMAIN = 'grademiners.com'


SESSION = HTMLSession()
QUEUE_VARIABLE = Queue()


def get_top():
    with open('keywords.csv', 'r', encoding='utf-8') as keywords_file:

        for keyword in keywords_file:
            QUEUE_VARIABLE.put(keyword)
            data_for_bd = {}
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            keyword = keyword.strip()
            url = f'https://www.google.com/search?q={keyword}&num={COUNT}&hl=en'
            response = SESSION.get(url)
            links = response.html.xpath('//div[@class="r"]/a[1]/@href')

            found = False

            for position, link in enumerate(links, start=1):

                if DOMAIN in link:
                    data_for_bd = {
                        'query': keyword,
                        'link': link,
                        'position': position,
                        'date': date
                    }
                    Top.create(**data_for_bd)
                    found = True
                    break

            if not found:
                data_for_bd = {
                    'query': keyword,
                    'link': 'not found',
                    'position': 0,
                    'date': date
                }
                Top.create(**data_for_bd)

            pprint(data_for_bd)
            print('[SCANNED]', keyword, f'[{response.status_code}]')

        print('All Done!')


def threads_script():
    for i in range(3):
        thread = Thread(target=get_top)
        thread.start()


if __name__ == "__main__":
    threads_script()
