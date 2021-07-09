import time

import requests
from bs4 import BeautifulSoup

ENDPOINT_URL = "https://www.kinopoisk.ru/popular/films/"
PARAMS = {
    "quick_filters": "serials",
    "tab": "all",
}


class Scraper:

    def __init__(self, start_url, start_params):
        self.start_url = start_url
        self.start_params = start_params
        self.serials_info = []

    def get_html_string(self, url, params):
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except Exception as e:
            print(e)
            return None
        return response.text

    def get_serial_info(self, serail):
        info = {}
        info['name'] = serail.find(attrs={
            "class": "selection-film-item-meta__name"
        }).text
        info['original_name'] = serail.find(attrs={
            "class": "selection-film-item-meta__original-name"
        }).text

        try:
            info['rating'] = serail.find(attrs={"class": "rating__value"}).text
            info['rating'] = float(info['rating'])
        except AttributeError as e:
            print(e)
        except ValueError as e:
            print(e)

        return info

    def run(self):
        self.paginate(self.start_url, self.start_params)

        for page in range(2, 7):
            params = self.start_params
            params["page"] = page
            self.paginate(self.start_url, params)
            time.sleep(1)
        # print(self.serials_info)
        # print(self.paginate(self.start_url, self.start_params))

        print(len(self.serials_info))

    def save_serials_info(self):
        pass

    def parse_page(self, response):
        pass

    # for page 2
    def paginate(self, url, params):

        html_string = self.get_html_string(url, params)
        if not html_string:
            print("Error!")
            return

        soup = BeautifulSoup(html_string, "html.parser")
        serials = soup.find_all(
            attrs={"class": "desktop-rating-selection-film-item"}
        )

        for serial in serials:
            self.serials_info.append(self.get_serial_info(serial))

        # paginator_element = soup.find(
        #     attrs={
        #         "class": "paginator__page-number",
        #     },
        #     text="2",
        # ).attrs["href"]
        # return paginator_element


if __name__ == "__main__":
    my_scraper = Scraper(ENDPOINT_URL, PARAMS)
    my_scraper.run()

# response = requests.get(
# "https://www.kinopoisk.ru/popular/films/?quick_filters=serials&tab=all")
#
# soup = BeautifulSoup(response.text, "html.parser")
#
# # section = soup.find_all("section", attrs={"class": "front"})
#
# section = soup.find_all("section")
#
# print(len(section))
#
# section_front = [
#     sect for sect in section if (sect.attrs.get('class')\
#     and 'front' in sect.attrs['class'])
# ]
