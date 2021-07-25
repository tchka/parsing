import scrapy
from lmscraper.items import LmscraperItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class LmspiderSpider(scrapy.Spider):
    name = 'lmspider'
    allowed_domains = ['leroymerlin.ru']
    start_urls = ['http://leroymerlin.ru/']

    def __init__(self, query, **kwargs):
        super().__init__(**kwargs)
        url = f'https://leroymerlin.ru/search/?q={query}'
        self.start_urls = [url]

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[@data-qa-product-image]')

        for link in links:
            print("LINK")
            print()
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath('//a[@data-qa-pagination-item="right"]\
                                   /@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        name_xpath = '//h1/text()'
        price_xpath = '//*[@itemprop="price"]/@content'
        big_image_xpath = '//uc-pdp-media-carousel/picture/source[1]/@srcset'
        parameters_xpath = '//dl[contains(@class,"def-list")]\
        /div[contains(@class,"def-list__group")]'
        parameters_tags = response.xpath(parameters_xpath)
        parameters = {}
        for parameters_tag in parameters_tags:
            key = parameters_tag.xpath('.//dt/text()').get()
            value = parameters_tag.xpath('.//dd/text()').get()
            value = value.replace('\n', '').strip()
            parameters[key] = value

        loader = ItemLoader(item=LmscraperItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', name_xpath)
        loader.add_xpath('price', price_xpath)
        loader.add_xpath('img_urls', big_image_xpath)
        loader.add_value('parameters', parameters)
        print("ITEM")
        print()
        yield loader.load_item()
