
from pprint import pprint

import requests
from fp.fp import FreeProxy
from lxml.html import fromstring
from pymongo import MongoClient

FP_OBJECT = FreeProxy()


def get_proxies():
    return FP_OBJECT.get_proxy_list()


def retry_request(url, headers, proxies_list, retry_number=3):
    for i in range(max(retry_number, len(proxies_list))):
        proxy = {
            "http": proxies_list[i]
        }
        try:
            response = requests.get(url, headers=headers, proxies=proxy)
            response.raise_for_status()
            if response.status_code == 200:
                return response

        except Exception as e:
            print(e)
            print(f'Exception on {i}-th retry')

    return None


def process_item_lenta(item):
    item_title = "./text()"
    item_time = "./time/@datetime"
    item_link = "./@href"

    info = {}
    try:
        info['source'] = "lenta.ru"
        info['title'] = clear_string(item.xpath(item_title)[0])
        info['link'] = item.xpath(item_link)[0]
        info['time'] = item.xpath(item_time)[0]
    except Exception as e:
        print(e)
        raise Exception(f'cant extract title on {item}')

    return info


def process_items_lenta(items):
    items_info = []
    try:
        for item in items:
            items_info.append(process_item_lenta(item))
    except Exception as e:
        print(e)

    return items_info


def save_mongo(items_info):
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_DB = "news"
    MONGO_COLLECTION = "Lenta"

    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        for item in items_info:
            set_value = {
                "$set": item
            }
            collection.update_one(item,
                                  set_value, upsert=True)


def pipeline_lenta(url, headers, proxies_list, retry_number=3):
    response = retry_request(url, headers, proxies_list, retry_number)
    if not response:
        return
    dom = fromstring(response.text)
    items_lenta = "//*[contains(@class, 'b-top7-for-main')]//\
    div[contains(@class, 'item')]/a[not(contains(@class, 'pic'))]"

    items = dom.xpath(items_lenta)
    items_info = process_items_lenta(items)

    save_mongo(items_info)

    pprint(items_info)


def clear_string(text):
    return text.replace('\xa0', ' ')


headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

url = "https://lenta.ru/"

proxies_list = get_proxies()
retry_number = 4
pipeline_lenta(url, headers, proxies_list, retry_number)
