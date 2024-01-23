import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.mySql_connection_pipeline import MySqlConnectionPipeline

class MySqlClubPipeline(MySqlConnectionPipeline):
  
  def process_item(self, item, spider):
    try:
      self.cur.execute("""
      INSERT INTO clubs(id, url, club_name, id_current_league, current_mv)
      VALUES(%s, %s, %s, %s, %s);
      """, (item['id'],item['url'], item['club_name'], item['current_league'], item['current_mv']))

      self.conn.commit()
      return item
    except mysql.connector.Error as e:
      raise DropItem(f'**mySQL error when inserting item: {e}')
  

  