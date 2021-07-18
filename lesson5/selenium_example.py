import os
import time
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

load_dotenv()

EMAIL = os.getenv('EMAIL1', None)
PASSWORD = os.getenv('PASSWORD')
DRIVER_PATH = '../chromedriver.exe'

url = 'https://gb.ru/login'

options = webdriver.ChromeOptions()
# options.add_argument('--window-size=1300,500')
options.add_argument('--start-maximized')

driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(url)
user_email_input = driver.find_element_by_id('user_email')
user_email_input.send_keys(EMAIL)

user_pass_input = driver.find_element_by_id('user_password')
# user_pass_input.send_keys(PASSWORD + "\n")
user_pass_input.send_keys(PASSWORD)
# user_pass_input.send_keys("\n")
user_pass_input.send_keys(Keys.ENTER)

url = 'https://gb.ru/profile'
driver.get(url)

city_input = driver.find_element_by_name('user[city]')
city_input.clear()
city_input.send_keys("Ойкумена")

gender_elem = driver.find_element_by_name('user[gender]')
gender_select = Select(gender_elem)
# time.sleep(5)
gender_select.select_by_index(2)
# time.sleep(5)
# gender_select.select_by_visible_text('Не выбран')
gender_elem.submit()

url = 'https://gb.ru/logout'
driver.get(url)

# close browser tab
# driver.close()

# close browser
time.sleep(10)
driver.quit()
