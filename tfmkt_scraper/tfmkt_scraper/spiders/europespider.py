import scrapy
from tfmkt_scraper.items import LeagueItem


class EuropespiderSpider(scrapy.Spider):
    name = "europespider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = ["https://www.transfermarkt.com/wettbewerbe/europa"]

    #Spider specific settings
    custom_settings = {
        'ITEM_PIPELINES': {
             "tfmkt_scraper.pipelines.league.league_pipeline.LeagueScraperPipeline": 300,
        },
        'FEEDS': {
            './data/leagues.json': {'format': 'json', 'overwrite': True}
        }
    }

    def parse(self, response):
        table_rows = response.css('table.items tbody tr.odd, table.items tbody tr.even')
        for row in table_rows:
            league_item = LeagueItem()
            league_realtive_url = row.css('a').attrib['href']
            league_url = 'https://www.transfermarkt.com' + league_realtive_url
            league_item['url'] = league_url
            league_item['league_current_mv'] = row.css('td.rechts.hauptlink::text').get()
            yield response.follow(league_url, callback= self.parse_league_page, cb_kwargs=dict(item=league_item))


        next_page = response.css('li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page ::attr(href)').get()
        if next_page is not None:
            next_page_url = 'https://www.transfermarkt.com' + next_page
            yield response.follow(next_page_url, callback= self.parse)


    def parse_league_page(self, response, item):
        league_name = response.css('h1.data-header__headline-wrapper.data-header__headline-wrapper--oswald::text').get()
        league_country =  response.css('span.data-header__club a::text').get()
        item['league_name'] = league_name
        item['league_country'] = league_country
        yield item
