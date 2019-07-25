from requests_html import HTMLSession
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


if __name__ == "__main__":
    parser_links_from_category_page()

