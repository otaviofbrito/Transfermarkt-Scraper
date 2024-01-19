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