import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tfmkt_scraper.items import ClubLeagueItem

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
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a', deny=[r'/profil/spieler/', 'pokalwettbewerb']), follow=False, callback='parse_league_page'),
        Rule(LinkExtractor(restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page',  deny=[r'/profil/spieler/', r'/pokalwettbewerb/']), follow=True)
    )
   
    

   def parse_league_page(self, response):
     if 'pokalwettbewerb' in response.url:
        print("***********>cup ignored")
        return
     
     league_url = response.url
     regex_match_league_id = re.search(r'/wettbewerb/([A-Z0-9]+)', league_url, re.IGNORECASE) 
     league_id = regex_match_league_id.group(1)

     seasons = response.xpath('//select[@class="chzn-select"]/option/@value')
     for season in seasons:
       season_url = league_url + '/plus/?saison_id=' + season.get() 
       yield response.follow(season_url, callback=self.parse_club_league)

       
  

   def parse_club_league(self, response):
      print("test")





      