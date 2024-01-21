# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TfmktScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LeagueItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    league_name = scrapy.Field()
    league_country = scrapy.Field()
    league_current_mv = scrapy.Field()

class ClubItem(scrapy.Item):
    url = scrapy.Field()
    id = scrapy.Field()
    club_name = scrapy.Field()
    current_league = scrapy.Field()
    current_mv = scrapy.Field()

class ClubLeagueItem(scrapy.Item):
    club_id = scrapy.Field()
    league_id = scrapy.Field()
    season = scrapy.Field()
    squad = scrapy.Field()
    market_value = scrapy.Field()


class TransferItem(scrapy.Item):
    player_id = scrapy.Field()
    year = scrapy.Field()
    left_club_id = scrapy.Field()
    joined_club_id = scrapy.Field()
    transfer_fee = scrapy.Field()
    transfer_type = scrapy.Field()  #0 - not loan, 1- loan, 2- end of loan, 3- unknown
    
    
    
class PlayerItem(scrapy.Item):
    id = scrapy.Field()
    url = scrapy.Field()
    name = scrapy.Field()
    full_name = scrapy.Field()
    birth_date = scrapy.Field()
    death_date = scrapy.Field()
    height = scrapy.Field()
    citizenship_1 = scrapy.Field()
    citizenship_2 = scrapy.Field()
    foot = scrapy.Field()
    agent = scrapy.Field()
    current_club = scrapy.Field()    
    outfitter = scrapy.Field()
    main_position = scrapy.Field()
    current_mv = scrapy.Field()
    
##TODO: save league and clubs logo