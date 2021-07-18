from selenium import webdriver

DRIVER_PATH = '../chromedriver.exe'
url = 'https://5ka.ru/special_offers/'

driver = webdriver.Chrome(DRIVER_PATH)

driver.get(url)
