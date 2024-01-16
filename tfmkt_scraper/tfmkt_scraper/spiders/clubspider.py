import scrapy


class ClubspiderSpider(scrapy.Spider):
    name = "clubspider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/wettbewerbe/europa"]

    def parse(self, response):
        pass
