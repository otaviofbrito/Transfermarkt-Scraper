import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.mySql_connection_pipeline import MySqlConnectionPipeline
class MySqlClub_LeaguePipeline(MySqlConnectionPipeline):

  def process_item(self, item, spider):
    try:
      self.cur.execute("""
      INSERT INTO club_league(club_id, league_id, season, squad, market_value)
      VALUES(%s, %s, %s, %s, %s);
      """, (item['club_id'],item['league_id'], item['season'], item['squad'], item['market_value']))

      self.conn.commit()
      return item
    except mysql.connector.Error as e:
      raise DropItem(f'**mySQL error when inserting item: {e}')