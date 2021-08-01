# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from igfollowscrapy.settings import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient

MONGO_DB = "ig"
MONGO_COLLECTION = "user_follow"


class IgfollowscrapyPipeline:

    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client[MONGO_DB]
        self.collection = self.db[MONGO_COLLECTION]

    def process_item(self, item, spider):
        if not self.collection.find_one(item):
            self.collection.insert_one(item)
        return item

    def close_spider(self):
        self.client.close()
