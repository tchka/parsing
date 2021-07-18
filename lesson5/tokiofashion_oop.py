import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

MONGO_HOST = "localhost"
MONGO_PORT = 27017
MONGO_DB = "vk"
MONGO_COLLECTION = "Tokiofashion"
ENDPOINT_URL = "https://vk.com/tokyofashion"
DRIVER_PATH = '../chromedriver.exe'


class ScraperVK:

    def __init__(self, url, string_to_search, max_scrolls, driver_path,
                 host, port, db_name, collection_name):
        self.url = url
        self.string_to_search = string_to_search
        self.max_scrolls = int(max_scrolls)
        self.driver_path = driver_path
        self.client = MongoClient(host, port)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

        self.options = webdriver.ChromeOptions()
        self.options.add_argument('--start-maximized')
        self.driver = webdriver.Chrome(driver_path, options=self.options)
        self.actions = ActionChains(self.driver)

    def scroll_to_myblock(self, myblock):
        try:
            self.actions.move_to_element(myblock).perform()
        except Exception as e:
            print(e)
            print('cannot perform move')

    def click_button_by_classname(self, button_class, timeout):
        button = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, button_class)
            )
        )
        button.click()

    def scroll_down(self, height):
        try:
            self.driver.execute_script(
                "window.scrollTo(0," + str(height) + ")"
            )
        except Exception as e:
            print(e)
            print(f'cannot move down {height}')

    def input_text_and_submit(self, input_id, timeout, text):
        input = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable(
                (By.ID, input_id)
            )
        )
        input.send_keys(text)
        input.send_keys(Keys.ENTER)

    def scroll_down_to_see_more(self):

        max_scrolls = 1
        i = 0

        while i < max_scrolls:
            try:
                self.driver.execute_script(
                    "window.scrollTo(0, document.body.scrollHeight)"
                )
                i += 1
                print(i)
            except Exception as e:
                print(e)

            time.sleep(12)

    def process_item(self, item, p):

        info = {}
        date = item.find_element_by_class_name('rel_date')
        info['date'] = date.text

        content = item.find_element_by_class_name('wall_post_text')
        info['content'] = content.text

        link = item.find_element_by_class_name('post_link')
        # print(link.get_attribute('href'))
        info['link'] = link.get_attribute('href')

        try:
            likes = item.find_element_by_xpath('.//*[contains(@class, "_like")]\
            /*[contains(@class, "like_button_count")]')
            # print(likes.text)
            info['likes'] = likes.text
        except Exception as e:
            print(e)
            print(f'No likes for {p}-th post')

        try:
            shares = item.find_element_by_xpath('.//*[contains(@class, "_share")]\
            /*[contains(@class, "like_button_count")]')
            # print(shares.text)
            info['shares'] = shares.text
        except Exception as e:
            print(e)
            print(f'No shares for {p}-th post')

        try:
            views_tag = item.find_element_by_class_name('_views')
            views = views_tag.text
            # print(views)
            info['views'] = views
        except Exception as e:
            print(e)
            print(f'No views for {p}-th post')

        return info

    def save_mongo(self, items_info):

        for item in items_info:
            if not self.collection.find_one(item):
                self.collection.insert_one(item)

    def run(self):

        self.driver.get(self.url)

        # Scroll page to the wall start
        wall_block = self.driver.find_element_by_class_name('wall_module')
        self.scroll_to_myblock(wall_block)

        # While scrolling we'll receive the blockin popup, close it
        self.click_button_by_classname('JoinForm__notNow', 60)

        time.sleep(3)

        # Scrolling doen to make search button interactable
        self.scroll_down(400)

        # click the search button
        self.click_button_by_classname('ui_tab_search', 1)

        time.sleep(3)

        # input the string to search
        self.input_text_and_submit('wall_search', 2, self.string_to_search)

        time.sleep(3)

        self.scroll_down_to_see_more()

        items_xpath = '//*[contains(@id, "page_search_posts")]\
        /div[contains(@class, "post")]'
        items = self.driver.find_elements_by_xpath(items_xpath)
        print(len(items))

        items_info = []
        p = 0
        for item in items:
            info = self.process_item(item, p)
            p += 1
            items_info.append(info)

        self.save_mongo(items_info)
        self.client.close()
        self.driver.quit()


if __name__ == '__main__':
    print('Searching VK page tokiofashion')
    string_to_search = input('Enter string to search: ')
    max_scrolls = input('Enter max pages to scroll down: ')

    my_scrapervk = ScraperVK(ENDPOINT_URL, string_to_search, max_scrolls,
                             DRIVER_PATH, MONGO_HOST, MONGO_PORT, MONGO_DB,
                             MONGO_COLLECTION)
    my_scrapervk.run()
