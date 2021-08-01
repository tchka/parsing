from instascrapy import settings
from instascrapy.spiders.instaspider import InstaspiderSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # users_to_parse = 'tati_001_'
    users_to_parse = 'vsemdobra_111'
    login = "tchka594"
    password = "#PWD_INSTAGRAM_BROWSER:10:1627501681:AYJQAI\
    7K5b04bgDly4Lrm08XOOU+TeR7qeR/0g26g8o4OTJyIPZPn7MhJZ/FMV\
    Eej1/tsLdJ0lx9oXYypABOBjS6cOF/3mXdXgMfkcVg8m7vPvpDoIDAavD\
    lEWv8u1rGnwfOo1XBkcrIwQ8e"

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(InstaspiderSpider, login=login, password=password,
                  users_to_parse=users_to_parse)
    process.start()
