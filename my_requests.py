from pprint import pprint

import requests

url = "http://www.google.ru"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko)"
}
response = requests.get(url, headers=headers)

print(response)
pprint(dict(response.headers))
pprint(response.headers['Content-Type'])
# pprint(response.headers['Content-Length'])
pprint(response.is_redirect)
# pprint(response.text)
