# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
# from itemadapter import ItemAdapter
from jobfinder.settings import MONGO_HOST, MONGO_PORT
from pymongo import MongoClient

MONGO_DB = "posts"
MONGO_COLLECTION = "news_posts"


class JobfinderPipeline:
    def __init__(self):
        self.client = MongoClient(MONGO_HOST, MONGO_PORT)
        self.db = self.client.vacancies

    def process_salary(self, salary):
        salary_min = None
        salary_max = None
        currency = None
        salary_as_list = salary[0].replace('\xa0', '').split(' ')
        print()

        if "от" in salary_as_list:
            i = salary_as_list.index('от')
            salary_min = ''
            while salary_as_list[1 + i].isdigit():
                salary_min += salary_as_list[1 + i]
                i += 1
                print()
            salary_min = int(salary_min)
            currency = salary_as_list[-1]

        if "до" in salary_as_list:
            i = salary_as_list.index('до')
            salary_max = ''
            while salary_as_list[1 + i].isdigit():
                salary_max += salary_as_list[1 + i]
                print()
                i += 1

            salary_max = int(salary_max)
            currency = salary_as_list[-1]

        return salary_min, salary_max, currency

    def sj_process_salary(self, salary):
        salary_min = None
        salary_max = None
        currency = None

        if len(salary) == 5:
            if salary[0] == 'от':
                salary_as_list = salary[2].split('\xa0')
                salary_min = salary_as_list[:-1]
                salary_min = ''.join(salary_min)
                salary_min = int(salary_min)
                currency = salary_as_list[-1]

            elif salary[0] == 'до':
                salary_as_list = salary[2].split('\xa0')
                salary_max = salary_as_list[:-1]
                salary_max = ''.join(salary_max)
                salary_max = int(salary_max)
                currency = salary_as_list[-1]

            else:
                salary_min = int(salary[0].replace('\xa0', ''))
                salary_max = salary_min
                currency = salary[2]

        elif len(salary) == 9:
            salary_min = int(salary[0].replace('\xa0', ''))
            salary_max = int(salary[4].replace('\xa0', ''))
            currency = salary[6]

        return salary_min, salary_max, currency

    def process_item(self, item, spider):
        if spider.name == 'hhru':
            item['source'] = spider.name
            item['salary_min'], item['salary_max'], item['currency'] =\
                self.process_salary(item['salary'])
            item.pop('salary')
            if not self.db[spider.name].find_one(item):
                self.db[spider.name].insert_one(item)
            return item

        elif spider.name == 'sjru':

            item['source'] = spider.name
            item['salary_min'], item['salary_max'], item['currency'] =\
                self.sj_process_salary(item['salary'])
            item.pop('salary')
            if not self.db[spider.name].find_one(item):
                self.db[spider.name].insert_one(item)
            return item

        return None

    def close_spider(self):
        self.client.close()
