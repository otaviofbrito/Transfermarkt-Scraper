BOT_NAME = "tfmkt"

SPIDER_MODULES = ["tfmkt_scraper.spiders"]
NEWSPIDER_MODULE = "tfmkt_scraper.spiders"

ROBOTSTXT_OBEY = False

AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_TARGET_CONCURRENCY = 5

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

# Neo4j SETTINGS
NEO4J_URI = "neo4j://neo4j:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "secretgraph"
NEO4J_DATABASE = "neo4j"

# HTTP CACHE SETTINGS
DOWNLOADER_MIDDLEWARES = {
    "scrapy.downloadermiddlewares.httpcache.HttpCacheMiddleware": 500
}

HTTPCACHE_ENABLED = True

LOG_LEVEL = 'WARNING'