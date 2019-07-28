import random
import datetime
from queue import Queue
from threading import Lock, Thread
# from multiprocessing import Process
# from concurrent.futures import ThreadPoolExecutor
from requests_html import HTMLSession
from create_db import Top

DOMAIN = 'grademiners.com'

with open('ua.txt', 'r', encoding='utf-8') as f:
    user_agents = f.read().split('\n')

with open('proxylist.txt', 'r', encoding='utf-8') as f:
    proxies_list = f.read().split('\n')


locker = Lock()


def get_response(url):
    with HTMLSession() as session:
        for _ in range(5):
            prox = random.choice(proxies_list)
            proxies = {'http': prox, 'https': prox}
            headers = {'User-Agent': random.choice(user_agents)}
            try:
                response = session.get(url, proxies=proxies,
                                       headers=headers, timeout=4)
                if response.status_code == 200:
                    break
                else:
                    response = None
            except Exception as e:
                print(e, type(e))
                response = None
    return response


def category_worker(qu):
    while True:
        url = qu.get()
        try:
            response = get_response(url)
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            links = response.html.xpath('//div[@class="r"]/a[1]/@href')

            for link in links:
                found = False

                if DOMAIN in link:
                    ad_dict = {
                        'link': link,
                        'date': date,
                    }
                    Top.create(**ad_dict)
                    found = True
                    break

                if not found:
                    ad_dict = {
                        'link': 'no position',
                        'date': date,
                    }
                    Top.create(**ad_dict)

        except Exception as e:
            print(e, type(e))
            qu.put(url)

        if qu.empty():
            break


def main():
    category_queue = Queue()
    workers_count = 100

    with open('grademiners.csv', 'r', encoding='utf-8') as keywords_file:
        keywords_list = keywords_file.read().split('\n')
        category_base_url = 'https://www.google.com/search?q={}&num=100&hl=en'

        for keyword in keywords_list:
            cat_url = category_base_url.format(keyword)
            category_queue.put(cat_url)

    for i in range(workers_count):
        tread = Thread(
            target=category_worker,
            args=(category_queue, )
        )
        tread.start()

    # with ThreadPoolExecutor(max_workers=workers_count) as executor:
    #     for _ in range(workers_count):
    #         executor.submit(category_worker, category_queue)


if __name__ == '__main__':
    main()