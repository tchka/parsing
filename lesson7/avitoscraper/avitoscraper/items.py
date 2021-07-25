# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Compose, MapCompose, TakeFirst


def clean_array(string_array):
    return ' '.join(map(lambda x: x.strip(), string_array))


def clean_string(url):
    return url.strip()


class AvitoscraperItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field(output_processor=TakeFirst())
    name = scrapy.Field(input_processor=Compose(clean_array),
                        output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    img_urls = scrapy.Field(input_processor=MapCompose(clean_string))
    img_info = scrapy.Field()
