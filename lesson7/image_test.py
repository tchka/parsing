from urllib.parse import quote_plus

import requests

url = "https://cdn.fishki.net/upload/post/201510/13/1695788/" \
      "0_116e6d_6fa9cc7d_orig.jpg"
query = quote_plus('материнская плата asus'.encode(encoding='cp1251'))
url1 = f'http://www.onlinetrade.ru/sitesearch.html?query={query}'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# def get_extension(headers):
#
#     if 'Content-Type' not in headers:
#         raise ValueError('No Content-Type in headers')
#
#     return headers['Content-Type'].split('/')[-1]
#
# response = requests.get(url, headers=headers)
# print(response.status_code)
# extension = get_extension(response.headers)
#
# with open(f'image.{extension}', 'wb') as f:
#     f.write(response.content)

response = requests.get(url1, headers=headers)
print()
