# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os

import scrapy
from lmscraper.settings import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient
from scrapy.pipelines.images import ImagesPipeline
from transliterate import slugify


class LmImagesPipeline(ImagesPipeline):

    def __init__(self, store_uri, download_func=None, settings=None):
        super().__init__(store_uri, settings=settings,
                         download_func=download_func)
        self.directory = ''

    def file_path(self, request, response=None, info=None):

        name = request.url.split('/')[-1]
        if name[-4:] != '.jpg':
            name = name + '.jpg'

        filename = os.path.join(self.directory, name)

        # print(filename)
        return filename

    def get_media_requests(self, item, info):
        self.directory = slugify(item['name'])
        if item['img_urls']:
            for img_url in item['img_urls']:
                try:
                    yield scrapy.Request(img_url)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['img_info'] = [
                x[1]
                for x in results
                if x[0]
            ]
        if item['img_urls']:
            del item['img_urls']
        # print('item_completed')
        # print()
        return item


class LmscraperPipeline:

    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.products

    def process_item(self, item, spider):
        item['source'] = spider.name
        if not self.db[spider.name].find_one(item):
            self.db[spider.name].insert_one(item)
        return item

    def close_spider(self):
        self.client.close()
