BOT_NAME = "tfmkt"

SPIDER_MODULES = ["tfmkt_scraper.spiders"]
NEWSPIDER_MODULE = "tfmkt_scraper.spiders"

ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

COOKIES_ENABLED = False


DOWNLOADER_MIDDLEWARES = {
    "tfmkt_scraper.middlewares.ScrapeOpsFakeBrowserHeaderAgentMiddleware": 543,
}



REQUEST_FINGERPRINTER_IMPLEMENTATION = "2.7"
TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"


# MY SQL SETTINGS
MYSQL_HOST = "mysql_db"
MYSQL_USER = "user"
MYSQL_PASSWORD = "user"
MYSQL_DATABASE = "tm_db"

#SCRAPE OPS -CFG FAKE HEADERS
SCRAPEOPS_API_KEY = '4bf0f201-a126-4646-baa6-d84d17f7531f' #APIKEY SCRAPEOPS
SCRAPEOPS_FAKE_USER_AGENT_ENDPOINT = 'https://headers.scrapeops.io/v1/user-agents'
SCRAPEOPS_FAKE_USER_AGENT_ENABLED = True
SCRAPEOPS_NUM_RESULTS = 5