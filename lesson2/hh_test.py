import requests
from fp.fp import FreeProxy

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


url = "https://hh.ru/search/vacancy"
# url = "https://ebay.com"

params = ({
    "area": "1",
    "fromSearchLine": "true",
    "st": "searchVacancy",
    "text": "python",
})

headers = {
    "User Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

proxies_list = get_proxies()
retry_number = 4

response = retry_request(url, headers, proxies_list, retry_number)
print(response)
# print(response.status_code)
