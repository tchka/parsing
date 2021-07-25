# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import scrapy
from scrapy.pipelines.images import ImagesPipeline


class AvitoImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
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
        print('item_completed')
        print()
        return item


class AvitoscraperPipeline:
    def process_item(self, item, spider):
        print('pipeline test')
        return item
