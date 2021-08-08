# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class InstascrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    id = scrapy.Field()
    user_id = scrapy.Field()
    username = scrapy.Field()
    image_url = scrapy.Field()
    metadata = scrapy.Field()
    likes = scrapy.Field()
