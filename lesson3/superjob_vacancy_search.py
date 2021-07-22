import re
import time

import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient

vacancy = input('Enter job keywords: ')
pages = input('Enter max pages to search : ')

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "vacancies"
MONGO_COLLECTION = "superjob"

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

    def __init__(self, start_url, headers, start_params, pages,
                 host, port, db_name, collection_name):
        self.start_url = start_url
        self.start_params = start_params
        self.headers = headers
        self.max_page_number = int(pages)
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

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
                    info["salary_min"] = int(salary_list[1] + salary_list[2])
                    return info
                if len(salary_list) == 4 and salary_list[0] == "до":
                    info["salary_max"] = int(salary_list[1] + salary_list[2])
                    return info
                if len(salary_list) == 3:
                    info["salary_min"] = int(salary_list[0] + salary_list[1])
                    info["salary_max"] = int(salary_list[0] + salary_list[1])
                    return info
                if len(salary_list) == 6:
                    info["salary_min"] = int(salary_list[0] + salary_list[1])
                    info["salary_max"] = int(salary_list[3] + salary_list[4])
                    return info

                else:
                    print(f'Salary string {salary_tag} \
                    not processed for {info["name"]}')
                    return info

        except AttributeError as e:
            print(elem)
            print(e)

    def run(self):
        self.parse_page(self.start_url, self.headers, self.start_params)
        page = 1

        while True:
            page += 1
            print(page)
            params = self.start_params
            params["page"] = page
            next = self.parse_page(self.start_url, self.headers, params)
            if (not next) or page >= self.max_page_number:
                break
            time.sleep(1)

        self.client.close()

    def parse_page(self, url, headers, params):

        html_string = self.get_html_string(url, headers, params)
        if not html_string:
            print("Error!")
            return

        soup = BeautifulSoup(html_string, "html.parser")
        vacancies = soup.find_all(attrs={"class": "f-test-search-result-item"})

        for vacancy in vacancies:
            vacancy_info = self.get_vacancy_info(vacancy)
            if vacancy_info:
                set_vacancy_value = {
                    "$set": vacancy_info
                }
                self.collection.update_one(vacancy_info,
                                           set_vacancy_value, upsert=True)

        paginator_element = soup.find(
            attrs={
                "rel": "next",
            },
        )
        return paginator_element


def vacancies_min_salary(min_salary):
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        cursor = collection.find({
            "$or": [
                {"salary_min": {"$gte": min_salary}},
                {"salary_max": {"$gte": min_salary}},
                {"salary": {"$gte": min_salary}},
            ]
        }, {"_id": 0})
        for vacancy in cursor:
            print(vacancy)


def vacancies_no_salary():
    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]
        cursor = collection.find({
            "$and": [
                {"salary_max": {"$exists": False}},
                {"salary_min": {"$exists": False}},
                {"salary": {"$exists": False}},
            ]
        }, {"_id": 0})
        for vacancy in cursor:
            print(vacancy)


if __name__ == "__main__":
    my_scraper = Scraper(ENDPOINT_URL, HEADERS, PARAMS, pages,
                         MONGO_HOST, MONGO_PORT, MONGO_DB, MONGO_COLLECTION)
    my_scraper.run()

    user_min_salary = int(input("Enter min salary: "))
    vacancies_min_salary(user_min_salary)
    vacancies_no_salary()
