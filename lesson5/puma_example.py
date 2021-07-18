from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

DRIVER_PATH = '../chromedriver.exe'
url = 'https://ru.puma.com/sportivnye-tovary-dlja-muzhchin.html'

options = webdriver.ChromeOptions()
# options.add_argument('--window-size=1300,500')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(url)

button_class = 'js-load-more'
ok = True

# while ok:
#     try:
#         button = driver.find_element_by_class_name(button_class)
#         button.click()
#     except Exception as e:
#         print(e)
#         ok = False

timeout = 120
i = 0
while i < 1:
    try:
        button = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(
                (By.CLASS_NAME, button_class)
            )
        )
        button.click()
        i += 1
        print(i)
    except Exception as e:
        print(e)
        ok = False

items_xpath = '//*[contains(@class, "product-item__details")]'
items = driver.find_elements_by_xpath(items_xpath)
print(len(items))
items_info = []

for item in items:
    title = item.find_element_by_class_name('product-item__name')
    print(title.text)
    items_info['title'] = title.text

source = driver.page_source
# process with lxml/BS4
