BOT_NAME = "tfmkt"

SPIDER_MODULES = ["tfmkt_scraper.spiders"]
NEWSPIDER_MODULE = "tfmkt_scraper.spiders"

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

COOKIES_ENABLED = False

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Windows; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.5060.114 Safari/537.36"

REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# MY SQL SETTINGS
MYSQL_HOST = "mysql_db"
MYSQL_USER = "user"
MYSQL_PASSWORD = "user"
MYSQL_DATABASE = "tm_db"


DOWNLOADER_MIDDLEWARES = {
    "tfmkt_scraper.middlewares.TfmktScraperDownloaderMiddleware": 543,
}
