import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor


class Club_LeagueSpider(CrawlSpider):
   name = "club_leaguespider"
   allowed_domains = ["www.transfermarkt.com"]
   start_urls = [
                 "https://www.transfermarkt.com/wettbewerbe/europa",
                 "https://www.transfermarkt.com/wettbewerbe/asien",
                 "https://www.transfermarkt.com/wettbewerbe/amerika",
                 "https://www.transfermarkt.com/wettbewerbe/afrika"
                ]
   
   rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a', deny=[r'/profil/spieler/', r'/pokalwettbewerb/']), follow=True),
        Rule(LinkExtractor(restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page',  deny=[r'/profil/spieler/', r'/pokalwettbewerb/']), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="box tab-print"]/div[last()]/a'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="large-4 columns"]/div[@class="box"]/a[last()-1]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="large-3 small-12 columns"]/table[@class="eigenetabelle"]/td[last()]/a'), callback='parse_club_page', follow=False)
    )
   
    

   def parse_club_page(self, response):
      club_url = response.url
      rankings_url = club_url.replace("startseite", "platzierungen")
      yield response.follow(rankings_url, callback=self.parse_ranking_page)

   def parse_ranking_page(self, response):
      yield{
         'club_url' : response.url,
         'season':  response.xpath('//div[@class="grid-view"]/table/tbody/tr[1]/td[1]/text()').get()
      }



      