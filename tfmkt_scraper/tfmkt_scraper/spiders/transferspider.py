import scrapy
import re
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from tfmkt_scraper.items import TransferItem
from tfmkt_scraper.utils import get_club_id, get_player_id

class TransferSpider(CrawlSpider):
    name = "transferspider"
    allowed_domains = ["www.transfermarkt.com"]
    start_urls = [
        "https://www.transfermarkt.com/wettbewerbe/europa",
        "https://www.transfermarkt.com/wettbewerbe/asien",
        "https://www.transfermarkt.com/wettbewerbe/amerika",
        "https://www.transfermarkt.com/wettbewerbe/afrika"
    ]

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//tr[@class="odd" or @class="even"]/td/table/tr/td[2]/a',  deny=['/profil/spieler/', '/pokalwettbewerb/']), follow=True),
        Rule(LinkExtractor(restrict_css='li.tm-pagination__list-item.tm-pagination__list-item--icon-next-page'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="box tab-print"]/div[last()]/a'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="large-4 columns"]/div[@class="box"]/a[last()-1]'), follow=True),
        Rule(LinkExtractor(restrict_xpaths='//div[@class="large-3 small-12 columns"]/table[@class="eigenetabelle"]/td[last()]/a'), callback='parse_club')
    )

    # Spider specific settings
    custom_settings = {
        'ITEM_PIPELINES': {
             "tfmkt_scraper.pipelines.transfer.transfer_pipeline.TransferScraperPipeline": 300,
             "tfmkt_scraper.pipelines.transfer.mySql_transfer_pipeline.MySqlTransferPipeline": 400,
        },
        'FEEDS': {
             './data/transfers.jsonl': {'format': 'jsonlines', 'overwrite': True},
             './data/transfers.csv': {'format': 'csv', 'overwrite': True}
        }
    }

    
    
    def parse_club(self, response):
        club_url = response.url
        transfers_url = club_url.replace('/startseite/', '/alletransfers/')
        yield response.follow(transfers_url, callback=self.parse_transfers)

    def parse_transfers(self, response):
        club_id = get_club_id(response.url)

        tables = response.xpath('//div[@class="box"]/table')
        if tables is None:
            print('********>No transfer table found!')
            return
        
        for table in tables:
          table_header = table.xpath('preceding-sibling::h2[1]/text()').get().strip()
          season_url = table.xpath('following-sibling::a[1]/@href').get()
          if season_url:
             match_season = re.search(r'\/saison_id\/(\d+)', season_url)
             season = match_season.group(1)
          else: season = None

          table_rows = table.xpath('tbody/tr')
          for row in table_rows:
              transfer_item = TransferItem()
              player_url = row.xpath('td[1]/a/@href').get()
              if player_url:
                  transfer_item['player_id'] = get_player_id(player_url)
              else:
                  transfer_item['player_id'] = None

              transfer_item['year'] = season

              away_club_url = row.xpath('td[3]/a/@href').get()
              if away_club_url:
                away_club_id = get_club_id(away_club_url)
              else:
                 away_club_id = -5 #retired

              if 'Arrivals' in table_header:
                transfer_item['joined_club_id'] = club_id
                transfer_item['left_club_id'] = away_club_id
              elif 'Departures' in table_header:
                transfer_item['joined_club_id'] = away_club_id
                transfer_item['left_club_id'] = club_id

              #0 - not loan, 1- loan, 2- end of loan, 3- unknown  
              fee = row.xpath('td[4]/text()').get()
              if fee:
                if 'loan transfer' in fee:
                   transfer_item['transfer_fee'] = 0
                   transfer_item['transfer_type'] = 1
                elif 'End of loan' in fee:
                   transfer_item['transfer_fee'] = 0
                   transfer_item['transfer_type'] = 2
                elif 'free transfer' in fee:
                   transfer_item['transfer_fee'] = 0
                   transfer_item['transfer_type'] = 0
                elif 'Loan fee' in fee:
                   value = row.xpath('td[4]/i/text()').get()
                   transfer_item['transfer_fee'] = value
                   transfer_item['transfer_type'] = 1
                elif '€' in fee:
                   transfer_item['transfer_fee'] = fee
                   transfer_item['transfer_type'] = 0
                else:
                   transfer_item['transfer_fee'] = 0
                   transfer_item['transfer_type'] = 3
              else:
                 transfer_item['transfer_fee'] = 0
                 transfer_item['transfer_type'] = 3


              yield transfer_item

              

          

         
          
       
