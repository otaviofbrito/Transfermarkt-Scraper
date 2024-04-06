from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging


def main():
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    spiders_names = ['leaguespider', 'clubspider']
    crawl(process, spiders_names)
    process.start()


def crawl(process: CrawlerProcess, spider_names: list):
    deferred = process.crawl(spider_names[0])
    if len(spider_names) > 1:
        deferred.addCallback(lambda _: crawl(process, spider_names[1:]))


if __name__ == '__main__':
    main()
