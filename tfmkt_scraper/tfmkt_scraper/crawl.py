from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import argparse
import sys


def main():
    parser = argparse.ArgumentParser()

    # Spider argument list
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--spider", nargs='+', help='List of spiders')

    # Optional storage arguments - Default is CSV only
    parser.add_argument("--csv", help='Store data in CSV', action="store_true")
    parser.add_argument(
        "--jsonl", help='Store data in JSONL', action="store_true")
    parser.add_argument(
        "--mysql", help='Store data in MYSQL DB', action="store_true")

    # Parse args
    args = parser.parse_args()

    storage_options = {
        'CSV': args.csv,
        'JSONL': args.jsonl,
        'MySQL': args.mysql
    }

    print("\n\t<-----------Transfermarkt Scraper----------->\n")
    settings = get_project_settings()
    process = CrawlerProcess(settings)
    spiders = process.spider_loader.list()

    if args.spider == None:
        selected_spiders = spiders
    else:
        selected_spiders = args.spider

    print("\n------Spiders selected: " +
          str(len(selected_spiders)) + "/" + str(len(spiders)))
    for name in selected_spiders:
        print(" - " + name)
    print("---------------------")

    print("\n------Storage selected: ")
    for key, value in storage_options.items():
        if value:
           print(" - " + key)
    print("---------------------\n")
    
    crawl(process, selected_spiders)
    process.start()


def crawl(process: CrawlerProcess, spiders: list):
    deferred = process.crawl(spiders[0])
    if len(spiders) > 1:
        deferred.addCallback(lambda _: crawl(process, spiders[1:]))


if __name__ == '__main__':
    main()
