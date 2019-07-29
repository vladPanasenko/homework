import random
import datetime
from queue import Queue
from requests_html import HTMLSession
from concurrent.futures import ThreadPoolExecutor
from create_db import Top

DOMAIN = 'grademiners.com'
keywords_list = []

with open('ua.txt', 'r', encoding='utf-8') as f:
    user_agents = f.read().split('\n')

with open('proxylist.txt', 'r', encoding='utf-8') as f:
    proxies_list = f.read().split('\n')

with open('grademiners.csv', 'r', encoding='utf-8') as keywords_file:
    for k in keywords_file:
        # keywords = keywords_file.read().split('\n')
        keywords_list.append(k)

keyword = keywords_list[0]


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
        keyword = qu.get()
        url = f'https://www.google.com/search?q={keyword}&num=100&hl=en'
        try:
            response = get_response(url)
            date = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            links = response.html.xpath('//div[@class="r"]/a[1]/@href')

            found = False

            for position, link in enumerate(links, start=1):

                if DOMAIN in link:
                    ad_dict = {
                        'link': link,
                        'date': date,
                        'position': position,
                        'keyword': keyword
                    }
                    Top.create(**ad_dict)
                    found = True

            if not found:
                ad_dict = {
                    'link': 'not found',
                    'date': date,
                    'position': 0,
                    'keyword': keyword
                }
                Top.create(**ad_dict)
        except Exception as e:
            print(e, type(e))
            qu.put(keyword)

        if qu.empty():
            break


queue = Queue()
workers_count = 100

for k in keywords_list:
    print(keywords_list)
    queue.put(k)

with ThreadPoolExecutor(max_workers=workers_count) as executor:
    for _ in range(workers_count):
        executor.submit(category_worker, queue)

