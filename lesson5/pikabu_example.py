import time

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

DRIVER_PATH = '../chromedriver.exe'
url = 'https://pikabu.ru/'

options = webdriver.ChromeOptions()
options.add_argument('--start-maximized')

driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(url)

for i in range(5):
    time.sleep(10)
    articles = driver.find_elements_by_tag_name('article')
    article = articles[-1]
    actions = ActionChains(driver)
    actions.move_to_element(article)
    # actions.key_down(Keys.CONTROL).key_down(Keys.END).key_up(Keys.END).key_up(Keys.CONTROL)
    # actions.send_keys(Keys.END)
    # driver.execute_script('some js')
    actions.perform()
