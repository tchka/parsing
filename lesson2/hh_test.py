import requests

url = "https://hh.ru/search/vacancy"
params = ({
    "area": "1",
    "fromSearchLine": "true",
    "st": "searchVacancy",
    "text": "python",
})

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
response = requests.get(url, headers=headers, params=params)
print(response.status_code)
