import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.mySql_connection_pipeline import MySqlConnectionPipeline


class MySqlLeaguePipeline(MySqlConnectionPipeline):

    def process_item(self, item, spider):
        try:
            self.cur.execute("""
      INSERT INTO leagues(id, url, league_name, country, current_mv)
      VALUES(%s, %s, %s, %s, %s);
      """, (item['id'], item['url'], item['league_name'], item['league_country'], item['league_current_mv']))

            self.conn.commit()
            return item
        except mysql.connector.Error as e:
            raise DropItem(f'**mySQL error when inserting item: {e}')
