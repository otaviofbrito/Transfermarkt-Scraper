from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import sys


def main():
    print("\n\t----TransferMarkt Scraper----\n")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    spiders = process.spider_loader.list()
    if len(sys.argv) <= 1:
        selected_spiders = spiders
    else:
        selected_spiders = sys.argv[1:]
    

    print("\n------Spiders selected: " + str(len(selected_spiders)) + "/" + str(len(spiders)))
    for name in selected_spiders:
        print(" - " + name)
    print("---------------------\n")
    crawl(process, selected_spiders)
    process.start()


def crawl(process: CrawlerProcess, spiders: list):
    deferred = process.crawl(spiders[0])
    if len(spiders) > 1:
        deferred.addCallback(lambda _: crawl(process, spiders[1:]))


if __name__ == '__main__':
    main()
