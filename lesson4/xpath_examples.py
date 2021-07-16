import re
from pprint import pprint

import requests
from fp.fp import FreeProxy
from lxml.html import fromstring

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


def process_item(item):
    ebay_item_title = ".//h3[contains(@class, 'item__title')]/text()"
    ebay_item_price = ".//*[contains(@class, 'price')]/text()"
    ebay_item_img = ".//img/@src"

    info = {}
    try:
        info['title'] = item.xpath(ebay_item_title)[0]
        info['price'] = item.xpath(ebay_item_price)
        info['img'] = item.xpath(ebay_item_img)[0]
    except Exception as e:
        print(e)
        raise Exception(f'cant extract title on {item}')

    return info


def process_items(items):
    items_info = []
    try:
        for item in items:
            items_info.append(process_item(item))
    except Exception as e:
        print(e)

    return items_info


def ebay_pipeline(url, headers, proxies_list, retry_number=3):
    response = retry_request(url, headers, proxies_list, retry_number)
    if not response:
        return
    dom = fromstring(response.text)
    ebay_items = "//ul[contains(@class, 'srp-results')]\
    //li//div[contains(@class, 's-item__wrapper')]"
    items = dom.xpath(ebay_items)
    items_info = process_items(items)
    pprint(items_info)


def clear_string(text):
    return re.sub(r'\xa0', '', text)


headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

url = "https://www.ebay.com/sch/i.html?\
_from=R40&_trksid=p2380057.m570.l2632&_nkw=skirts&_sacat=15724"

proxies_list = get_proxies()
retry_number = 4
ebay_pipeline(url, headers, proxies_list, retry_number)

# ebay_items = "//ul[contains(@class, 'srp-results')]\
# //li//div[contains(@class, 's-item__wrapper')]"
# ebay_item_title = ".//h3[contains(@class, 'item__title')]/text()"
# ebay_item_price = ".//*[contains(@class, 'price')]/text()"
# ebay_item_img = ".//img/@src"
#
# response = requests.get(url, headers=headers)
# print(response)
# dom = fromstring(response.text)
# items_info = []
# for item in dom.xpath(ebay_items):
#     info = {}
#     try:
#         info['title'] = item.xpath(ebay_item_title)[0]
#         info['price'] = item.xpath(ebay_item_price)
#         info['img'] = item.xpath(ebay_item_img)[0]
#     except Exception as e:
#         print(e)
#         continue
#
#     # print(type(str(item.xpath(ebay_item_price)[0])))
#     items_info.append(info)
#
# # pprint(items_info)
# print(len(items_info))
