import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ClubspiderSpider(CrawlSpider):
    name = "clubspider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = [
                 "https://www.transfermarkt.com/wettbewerbe/europa"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tbody/tr/td[2]/a'), follow=False),
        Rule(LinkExtractor(restrict_xpaths='//li[@id="tables"]/div/div/div[2]/ul[@class="list_unstyled"]/li[last()-1]/a'), follow=False),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="large-3 small-12 columns"]/table/tbody/tr/td[last()]/a'), callback='parse_club', follow=False)
    )

   
    def parse_club(self, response):
        yield{
            'name': response.css('h1.data-header__headline-wrapper.data-header__headline-wrapper--oswald::text').get().strip()
        }