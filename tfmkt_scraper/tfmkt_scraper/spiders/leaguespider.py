import scrapy
import re
from tfmkt_scraper.items import LeagueItem
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor



class LeagueSpider(CrawlSpider):
    name = "leaguespider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = [
                 "https://www.transfermarkt.com/wettbewerbe/europa",
                 "https://www.transfermarkt.com/wettbewerbe/asien",
                 "https://www.transfermarkt.com/wettbewerbe/amerika",
                 "https://www.transfermarkt.com/wettbewerbe/afrika"
                  ]
    
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a', deny=['/profil/spieler/', '/pokalwettbewerb/']), callback='parse_league_page'),
        Rule(LinkExtractor(restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page'), follow=True),
    )

    # Spider specific settings
    custom_settings = {
        'ITEM_PIPELINES': {
            "tfmkt_scraper.pipelines.league.league_pipeline.LeagueScraperPipeline": 300,
            "tfmkt_scraper.pipelines.league.mySql_league_pipeline.MySqlLeaguePipeline": 400
        },
        'FEEDS': {
            './data/leagues.jsonl': {'format': 'jsonlines', 'overwrite': True},
            './data/leagues.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    def parse_league_page(self, response):
        ## ignore cup pages
        league_url = response.url
        if '/pokalwettbewerb/' in league_url:
            print("***********>cup ignored")
            return 
        league_item = LeagueItem()
        
        regex_match_id = re.search(r'/wettbewerb/([A-Z0-9]+)', league_url, re.IGNORECASE) 
        league_item['id'] = regex_match_id.group(1)
        league_item['url'] = league_url

        league_name = response.css(
            'h1.data-header__headline-wrapper.data-header__headline-wrapper--oswald::text').get()
        league_country = response.css('span.data-header__club a::text').get()
        league_item['league_name'] = league_name
        league_item['league_country'] = league_country

        mv = response.xpath('//div[@class="data-header__box--small"]/a/text()[2]').get()
        ## get the 10 power value
        league_item['league_current_mv'] = mv
        if mv: 
           mv_pow = response.xpath('//div[@class="data-header__box--small"]/a/span[last()]/text()').get()
           league_item['league_current_mv'] = mv + mv_pow

        yield league_item
