import scrapy
from scrapy.http import HtmlResponse


class OtspiderSpider(scrapy.Spider):
    name = 'otspider'
    allowed_domains = ['onlinetrade.ru']

    start_urls = ['https://www.onlinetrade.ru']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        url = f'https://www.onlinetrade.ru/sitesearch.html?query={query}'
        self.start_urls = [url]

    def parse(self, response: HtmlResponse):
        print()
