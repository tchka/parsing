import scrapy
from jobfinder.items import JobfinderItem
from jobfinder.selectors import SJ_ITEM_SELECTOR, SJ_NAVIGATION_SELECTORS
from scrapy.http import HtmlResponse


class SjruSpider(scrapy.Spider):
    name = 'sjru'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://russia.superjob.ru/vacancy/search/?keywords=python']

    def parse(self, response: HtmlResponse):
        item_urls = response.xpath(SJ_NAVIGATION_SELECTORS['parse_item']) \
            .getall()
        for link in item_urls:
            # print(link)
            # print()
            yield response.follow(link, callback=self.parse_item)

        next_page = response.xpath(SJ_NAVIGATION_SELECTORS['parse']).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_item(self, response: HtmlResponse):
        # title = response.xpath(ITEM_SELECTORS['title']).get()
        # salary = response.xpath(ITEM_SELECTORS['salary']).getall()
        item = JobfinderItem()
        item['url'] = response.url
        for key, xpath in SJ_ITEM_SELECTOR.items():
            item[key] = response.xpath(xpath)

        item['title'] = item['title'].get()
        item['salary'] = item['salary'].getall()
        # print()
        yield item
