import time

from pymongo import MongoClient
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def save_mongo(items_info):
    MONGO_HOST = "localhost"
    MONGO_PORT = 27017
    MONGO_DB = "vk"
    MONGO_COLLECTION = "Tokiofashion"

    with MongoClient(MONGO_HOST, MONGO_PORT) as client:
        db = client[MONGO_DB]
        collection = db[MONGO_COLLECTION]

        for item in items_info:
            if not collection.find_one(item):
                collection.insert_one(item)


DRIVER_PATH = '../chromedriver.exe'
url = 'https://vk.com/tokyofashion'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')
driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(url)
actions = ActionChains(driver)

# Scroll page to the wall start
wall_block = driver.find_element_by_class_name('wall_module')
try:
    actions.move_to_element(wall_block).perform()
except Exception as e:
    print(e)
    print('cannot move to wall')

# While scrolling we'll receive the blockin popup, close it
timeout = 60
button_not_now_class = 'JoinForm__notNow'
button = WebDriverWait(driver, timeout).until(
    EC.element_to_be_clickable(
        (By.CLASS_NAME, button_not_now_class)
    )
)
button.click()

# Scrolling doen to make search button interactable
time.sleep(3)
try:
    driver.execute_script("window.scrollTo(0, 400)")
except Exception as e:
    print(e)
    print('cannot move down 400')

# click to search button
time.sleep(3)
button = driver.find_element_by_class_name('ui_tab_search')
button.click()

# input the string to search
input_search_id = 'wall_search'
input_search = WebDriverWait(driver, timeout).until(
    EC.element_to_be_clickable(
        (By.ID, input_search_id)
    )
)
input_search.send_keys("Дизайнер")
input_search.send_keys(Keys.ENTER)
time.sleep(2)

# scroll to see more posts, max_scrolls is integer \
# for maximum scroll to bottom attempts

max_scrolls = 1
i = 0

while i < max_scrolls:
    time.sleep(12)
    try:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        i += 1
        print(i)
    except Exception as e:
        print(e)

items_xpath = '//*[contains(@id, "page_search_posts")]\
/div[contains(@class, "post")]'
items = driver.find_elements_by_xpath(items_xpath)
print(len(items))
items_info = []
p = 0

for item in items:
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
        if likes:
            info['likes'] = likes.text
    except Exception as e:
        print(e)
        print(f'No likes for {p}-th post')

    try:
        shares = item.find_element_by_xpath('.//*[contains(@class, "_share")]\
        /*[contains(@class, "like_button_count")]')
        # print(shares.text)
        if shares:
            info['shares'] = shares.text
    except Exception as e:
        print(e)
        print(f'No shares for {p}-th post')

    try:
        views_tag = item.find_element_by_class_name('_views')
        views = views_tag.text
        # print(views)
        if views:
            info['views'] = views
    except Exception as e:
        print(e)
        print(f'No views for {p}-th post')

    p += 1
    items_info.append(info)

save_mongo(items_info)
