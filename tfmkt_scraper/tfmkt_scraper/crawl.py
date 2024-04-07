from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys


def main():
    print("\n\t----TransferMarkt Scraper----\n")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    if len(sys.argv) <= 1:
        spiders_names = process.spider_loader.list()
    else:
        spiders_names = sys.argv[1:]
    

    print("\n------Spiders selected: " + str(len(spiders_names)) + "/5")
    for name in spiders_names:
        print(" - " + name)
    print("---------------------\n")
    crawl(process, spiders_names)
    process.start()


def crawl(process: CrawlerProcess, spider_names: list):
    deferred = process.crawl(spider_names[0])
    if len(spider_names) > 1:
        deferred.addCallback(lambda _: crawl(process, spider_names[1:]))


if __name__ == '__main__':
    main()
