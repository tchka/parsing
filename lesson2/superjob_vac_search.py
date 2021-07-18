import json
import re
import time

import requests
from bs4 import BeautifulSoup

vacancy = input('Enter job keywords: ')
pages = input('Enter max pages to search : ')

ENDPOINT_URL = "https://russia.superjob.ru/vacancy/search/"
PARAMS = ({
    # "geo%5Bt%5D%5B0%5D": "4",
    # "geo%5Bo%5D%5B0%5D": "46",
    "keywords": vacancy,
})
HEADERS = {
    "User Agent": "Mozilla/5.0 (Windows NT 6.2; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}


class Scraper:

    def __init__(self, start_url, headers, start_params, pages):
        self.start_url = start_url
        self.start_params = start_params
        self.headers = headers
        self.max_page_number = int(pages)
        self.vacancies_list = []

    def clear_string(self, text):
        text_as_list = re.split(r'\xa0', text)
        return text_as_list

    def get_html_string(self, url, headers, params):
        try:
            response = requests.get(url, headers=headers, params=params)
            print(response)
            response.raise_for_status()
        except Exception as e:
            time.sleep(1)
            print(e)
            return None
        return response.text

    def get_vacancy_info(self, elem):
        info = {}

        try:
            name_tag = elem.find('a', attrs={
                "target": "_blank"
            })

            if name_tag:
                info["name"] = name_tag.text
                info["link"] = name_tag.attrs["href"]

            salary_tag = elem.find(attrs={
                "class": "f-test-text-company-item-salary"
            })
            if salary_tag:
                salary_list = self.clear_string(salary_tag.text)
                if salary_list[0] == "По договорённости":
                    return info
                if len(salary_list) == 4 and salary_list[0] == "от":
                    info["salary_min"] = salary_list[1] + salary_list[2]
                    return info
                if len(salary_list) == 4 and salary_list[0] == "до":
                    info["salary_max"] = salary_list[1] + salary_list[2]
                    return info
                if len(salary_list) == 3:
                    info["salary_min"] = salary_list[0] + salary_list[1]
                    info["salary_max"] = salary_list[0] + salary_list[1]
                    return info
                if len(salary_list) == 6:
                    info["salary_min"] = salary_list[0] + salary_list[1]
                    info["salary_max"] = salary_list[3] + salary_list[4]
                    return info

                else:
                    print(f'Salary string {salary_tag} \
                    not processed for {info["name"]}')
                    return info

        except AttributeError as e:
            print(elem)
            print(e)

    def save(self, dict):
        with open("vacancies_found.json", "w", encoding="utf-8") as f:
            json.dump(dict, f)

    def run(self):
        self.paginate(self.start_url, self.headers, self.start_params)
        page = 1

        while True:
            page += 1
            print(page)
            params = self.start_params
            params["page"] = page
            next = self.paginate(self.start_url, self.headers, params)
            if (not next) or page >= self.max_page_number:
                break
            time.sleep(1)

        print((self.vacancies_list))
        print(len(self.vacancies_list))
        data = {
            "source": ENDPOINT_URL,
            "search string": vacancy,
            "vacancies": self.vacancies_list,
        }
        self.save(data)

    def paginate(self, url, headers, params):

        html_string = self.get_html_string(url, headers, params)
        if not html_string:
            print("Error!")
            return

        soup = BeautifulSoup(html_string, "html.parser")
        vacancies = soup.find_all(attrs={"class": "f-test-search-result-item"})

        for vacancy in vacancies:
            self.vacancies_list.append(self.get_vacancy_info(vacancy))

        paginator_element = soup.find(
            attrs={
                "rel": "next",
            },
        )
        return paginator_element


if __name__ == "__main__":
    my_scraper = Scraper(ENDPOINT_URL, HEADERS, PARAMS, pages)
    my_scraper.run()
