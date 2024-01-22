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
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a', deny=[
             r'/profil/spieler/', 'pokalwettbewerb']), follow=False, callback='parse_league_page'),
        Rule(LinkExtractor(restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page',
             deny=[r'/profil/spieler/', r'/pokalwettbewerb/']), follow=True)
    )

    custom_settings = {
        'ITEM_PIPELINES': {
            "tfmkt_scraper.pipelines.club_league.club_league_pipeline.ClubLeagueScraperPipeline": 300,
            "tfmkt_scraper.pipelines.club_league.mySql_club_league_pipeline.MySqlClub_LeaguePipeline": 400
        },
        'FEEDS': {
            './data/club_league.jsonl': {'format': 'jsonlines', 'overwrite': True},
            './data/club_league.csv': {'format': 'csv', 'overwrite': True}
        }
    }
   

    def parse_league_page(self, response):
        if 'pokalwettbewerb' in response.url:
            print("***********>cup ignored")
            return
        
        league_url = response.url
        regex_match_league_id = re.search(
            r'/wettbewerb/([A-Z0-9]+)', league_url, re.IGNORECASE)
        league_id = regex_match_league_id.group(1)
        # Clear the url if the response url is from a season
        pattern = re.compile(r'/plus/\?saison_id=\d+')
        url_match = pattern.findall(league_url)
        if url_match:
            league_url = re.sub(pattern, '', league_url)

        seasons = response.xpath(
            '//select[@class="chzn-select"]/option/@value')
        for season in seasons:
            season = season.get()
            season_url = league_url + '/plus/?saison_id=' + season
            yield response.follow(season_url, callback=self.parse_club_league, cb_kwargs=dict(partial_data={'league_id': league_id, 'season': season}))


    def parse_club_league(self, response, partial_data):
        table_rows = response.xpath('//div[@id="yw1"]/table/tbody/tr')
        for row in table_rows:
            item = ClubLeagueItem()
            item['league_id'] = partial_data['league_id']
            item['season'] = partial_data['season']
            
            club_path = row.xpath('td[2]/a[1]/@href').get()
            regex_match_id = re.search(r'\/verein\/(\d+)', club_path, re.IGNORECASE)
            club_id = regex_match_id.group(1)
            item['club_id'] = club_id

            item['squad'] = row.xpath('td[3]/a[1]/text()').get()
            item['market_value'] = row.xpath('td[7]/a[1]/text()').get()

            yield item
