import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tfmkt_scraper.items import ClubItem


class PlayerSpider(CrawlSpider):
    name = "playerspider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = [
        "https://www.transfermarkt.com/wettbewerbe/europa",
        "https://www.transfermarkt.com/wettbewerbe/asien",
        "https://www.transfermarkt.com/wettbewerbe/amerika",
        "https://www.transfermarkt.com/wettbewerbe/afrika"
    ]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a',  deny=['/pokalwettbewerb/']), follow=True),
        Rule(LinkExtractor(
            restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="box tab-print"]/div[last()]/a'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="large-4 columns"]/div[@class="box"]/a[last()-1]'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="large-3 small-12 columns"]/table[@class="eigenetabelle"]/td[last()]/a'), callback='parse_club', follow=True),
        Rule(LinkExtractor(allow=r'\/profil\/spieler\/(\d+)$'), callback='parse_player', follow=False)
    )

    def parse_club(self, response):
        club_url = response.url
        players_url = re.sub(r'startseite', 'alumni', club_url)
        response.follow(players_url)


    def parse_player(self, response):
        yield {
            'url': response.url
        }