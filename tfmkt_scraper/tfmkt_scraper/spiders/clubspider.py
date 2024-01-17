import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class ClubspiderSpider(CrawlSpider):
    name = "clubspider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = [
                 "https://www.transfermarkt.com/wettbewerbe/europa"]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a', deny='/profil/spieler/'), follow=False, callback='parse_club'),
        Rule(LinkExtractor(restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page', deny='/profil/spieler/'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="box tab-print"]/div[last()]/a'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="large-4 columns"]/div[@class="box"]/a[last()-1]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="large-3 small-12 columns"]/table[@class="eigenetabelle"]/td[last()]/a'), callback='parse_club', follow=False)
    )


   
    def parse_club(self, response):
        yield{
            'url': response.url
        }

