import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tfmkt_scraper.items import ClubItem


class ClubspiderSpider(CrawlSpider):
    name = "clubs"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = [
        "https://www.transfermarkt.com/wettbewerbe/europa",
        "https://www.transfermarkt.com/wettbewerbe/asien",
        "https://www.transfermarkt.com/wettbewerbe/amerika",
        "https://www.transfermarkt.com/wettbewerbe/afrika"
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a', deny=[
             '/profil/spieler/', '/pokalwettbewerb/']), follow=True),
        Rule(LinkExtractor(
            restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="box tab-print"]/div[last()]/a'), follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@class="large-4 columns"]/div[@class="box"]/a[last()-1]'), follow=True),
        Rule(LinkExtractor(allow=r'\/startseite\/verein\/(\d+)$'),
             callback='parse_club')
    )

    # Spider specific settings
    custom_settings = {
        'ITEM_PIPELINES': {
            "tfmkt_scraper.pipelines.club.club_pipeline.ClubScrapperPipeline": 300,
            "tfmkt_scraper.pipelines.club.mySql_club_pipeline.MySqlClubPipeline": 400,
            "tfmkt_scraper.pipelines.club.neo4j_club_pipeline.Neo4jClubPipeline": 420
        },
        'FEEDS': {
            './data/clubs.jsonl': {'format': 'jsonlines', 'overwrite': True},
            './data/clubs.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    def parse_club(self, response):
        club_item = ClubItem()
        url = response.url
        # extract the id from the url
        regex_match_id = re.search(r'\/verein\/(\d+)', url, re.IGNORECASE)
        club_id = regex_match_id.group(1)
        club_item['id'] = club_id
        club_item['url'] = url

        club_item['club_name'] = response.css(
            'h1.data-header__headline-wrapper.data-header__headline-wrapper--oswald::text').get()

        league_path = response.css(
            'span.data-header__club a::attr(href)').get()
        if league_path:
            regex_match_current_league_id = re.search(
                r'/wettbewerb/([A-Z0-9]+)$',  league_path, re.IGNORECASE)
            league_id = regex_match_current_league_id.group(1)
            club_item['current_league'] = league_id
        else:
            club_item['current_league'] = None

        mv = response.xpath(
            '//div[@class="data-header__box--small"]/a/text()').get()
        # get the 10 power value
        club_item['current_mv'] = mv
        if mv:
            mv_pow = response.xpath(
                '//div[@class="data-header__box--small"]/a/span[last()]/text()').get()
            club_item['current_mv'] = mv + mv_pow

        yield club_item
