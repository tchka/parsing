# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IgfollowscrapyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    _id = scrapy.Field()
    status = scrapy.Field()
    username = scrapy.Field()
    follow_username = scrapy.Field()
    follow_user_id = scrapy.Field()
    follow_user_avatar_url = scrapy.Field()
