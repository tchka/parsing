from igfollowscrapy import settings
from igfollowscrapy.spiders.igfollow import IgfollowSpider
from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    # query = input('Введите поисковый запрос: ')
    # query = quote_plus(query.encode(encoding='utf8'))
    # users_to_parse = 'mirvsem_777 oksana6684'
    users_to_parse = input('Введите пользователей через пробел: ')
    # url = f'https://leroymerlin.ru/search/?q={query}'

    login = "tchka594"
    password = "#PWD_INSTAGRAM_BROWSER:10:1627501681:AYJQAI7K5b04bgD\
    ly4Lrm08XOOU+TeR7qeR/0g26g8o4OTJyIPZPn7MhJZ/FMVEej1/tsLdJ0lx9oXY\
    ypABOBjS6cOF/3mXdXgMfkcVg8m7vPvpDoIDAavDlEWv8u1rGnwfOo1XBkcrIwQ8e"

    process = CrawlerProcess(settings=crawler_settings)
    process.crawl(IgfollowSpider, login=login, password=password,
                  users_to_parse=users_to_parse)
    process.start()
