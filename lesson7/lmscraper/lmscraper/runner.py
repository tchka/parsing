from urllib.parse import quote_plus

from lmscraper import settings
from lmscraper.spiders.lmspider import LmspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    query = input('Введите поисковый запрос: ')
    query = quote_plus(query.encode(encoding='utf8'))
    # query = quote_plus('краска по металлу черная'.encode(encoding='utf8'))
    url = f'https://leroymerlin.ru/search/?q={query}'

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(LmspiderSpider, query=query)
    process.start()
