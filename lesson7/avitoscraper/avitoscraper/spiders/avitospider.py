import scrapy
from avitoscraper.items import AvitoscraperItem
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader


class AvitospiderSpider(scrapy.Spider):
    name = 'avitospider'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/moskva_i_mo?q=%D0%BA%D0%BE%D1%82']

    def parse(self, response: HtmlResponse):
        links = response.xpath('//a[contains(@class, "-item-title")]')

        for link in links[:1]:
            print("LINK")
            print()

            yield response.follow(link, callback=self.parse_item)

    def parse_item(self, response: HtmlResponse):
        name_xpath = '//h1/*[@itemprop="name"]/text()'
        price_xpath = '//*[@itemprop="price"]/@content'
        big_image_xpath = '//*[contains(@class, "gallery-img-frame")]' \
                          '/@data-url'
        # item = AvitoscraperItem()
        # item['name'] = response.xpath(name_xpath).get()
        # item['price'] = response.xpath(price_xpath).get()
        # item['img_urls'] = response.xpath(big_image_xpath).getall()
        # yield item

        loader = ItemLoader(item=AvitoscraperItem(), response=response)
        loader.add_value('url', response.url)
        loader.add_xpath('name', name_xpath)
        loader.add_xpath('price', price_xpath)
        loader.add_xpath('img_urls', big_image_xpath)
        print("ITEM")
        print()
        yield loader.load_item()
