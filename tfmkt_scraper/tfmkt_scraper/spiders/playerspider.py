import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tfmkt_scraper.items import PlayerItem


class PlayerSpider(CrawlSpider):
    name = "players"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = [
        "https://www.transfermarkt.com/wettbewerbe/europa",
        "https://www.transfermarkt.com/wettbewerbe/asien",
        "https://www.transfermarkt.com/wettbewerbe/amerika",
        "https://www.transfermarkt.com/wettbewerbe/afrika"
    ]

    rules = (
        Rule(LinkExtractor(
            restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a', deny=['/pokalwettbewerb/']), callback='parse_league'),
        Rule(LinkExtractor(
            restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page'), follow=True),
        Rule(LinkExtractor(allow=r'\/startseite\/verein\/(\d+)$'),
             callback='parse_club'),
        Rule(LinkExtractor(allow=r'\/profil\/spieler\/(\d+)$'),
             callback='parse_player')
    )

    custom_settings = {
        'ITEM_PIPELINES': {
            "tfmkt_scraper.pipelines.player.player_pipeline.PlayerScraperPipeline": 300,
            "tfmkt_scraper.pipelines.player.mySql_player_pipeline.MySqlPlayerPipeline": 400,
            "tfmkt_scraper.pipelines.player.neo4j_player_pipeline.Neo4jPlayerPipeline": 420
        },
        'FEEDS': {
            './data/player.jsonl': {'format': 'jsonlines', 'overwrite': True},
            './data/player.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    def parse_league(self, response):
        league_url = response.url
        clubs_table_url = re.sub(r'startseite', 'eigenetabelle', league_url)
        yield response.follow(clubs_table_url)

    def parse_club(self, response):
        club_url = response.url
        players_url = re.sub(r'startseite', 'alletransfers', club_url)
        yield response.follow(players_url)

    def parse_player(self, response):
        item = PlayerItem()
        player_url = response.url
        regex_match_payer_id = re.search(
            r'\/profil\/spieler\/(\d+)', player_url, re.IGNORECASE)
        item['id'] = regex_match_payer_id.group(1)
        item['url'] = player_url

        item['name'] = response.xpath(
            '//img[@class="data-header__profile-image"]/@alt').get()
        item['full_name'] = response.xpath(
            "//span[text()='Name in home country:' or text()='Full name:']/following::span[1]/text()").get()
        item['birth_date'] = response.xpath(
            "//span[@itemprop='birthDate']/text()").get()
        item['death_date'] = response.xpath(
            "//span[@itemprop='deathDate']/text()").get()
        item['height'] = response.xpath(
            "//span[@itemprop='height']/text()").get()

        citizenship = response.xpath(
            "//span[text()='Citizenship:']/following::span[1]/img/@title").getall()

        item['citizenship_1'] = None
        item['citizenship_2'] = None
        if len(citizenship) > 0:
            item['citizenship_1'] = citizenship[0]
        if len(citizenship) > 1:
            item['citizenship_2'] = citizenship[1]

        item['foot'] = response.xpath(
            "//span[text()='Foot:']/following::span[1]/text()").get()
        item['agent'] = response.xpath(
            "//span[text()='Player agent:']/following::span[1]/a/text()").get()

        current_club_url = response.xpath(
            '//span[@class="data-header__club"]/a/@href').get()

        if current_club_url:
            regex_match_id = re.search(
                r'\/verein\/(\d+)', current_club_url, re.IGNORECASE)
            item['current_club'] = regex_match_id.group(1)
        else:
            item['current_club'] = None

        item['outfitter'] = response.xpath(
            "//span[text()='Outfitter:']/following::span[1]/text()").get()

        item['main_position'] = response.xpath(
            "//span[text()='Position:']/following::span[1]/text()").get()

        mv = response.xpath(
            '//div[@class="data-header__box--small"]/a/text()').get()
        # get the 10 power value
        item['current_mv'] = mv
        if mv:
            mv_pow = response.xpath(
                '//div[@class="data-header__box--small"]/a/span[last()]/text()').get()
            item['current_mv'] = mv + mv_pow

        yield item
