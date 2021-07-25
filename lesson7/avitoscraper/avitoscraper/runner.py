from urllib.parse import quote_plus

from avitoscraper import settings
from avitoscraper.spiders.avitospider import AvitospiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    query = quote_plus('материнская плата asus'.encode(encoding='cp1251'))
    url = f'http://www.onlinetrade.ru/sitesearch.html?query={query}'

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(AvitospiderSpider, query=query)
    process.start()
