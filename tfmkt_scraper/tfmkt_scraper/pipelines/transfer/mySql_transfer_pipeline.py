import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.mySql_connection_pipeline import MySqlConnectionPipeline

class MySqlTransferPipeline(MySqlConnectionPipeline):

    def process_item(self, item, spider):
        try:
            self.cur.execute("""
      INSERT INTO transfers(
                              player_id,
                              year,
                              left_club_id,
                              joined_club_id,
                              transfer_fee,
                              transfer_type
                        )
      VALUES(%s, %s, %s, %s, %s, %s);
      """, (
                item['player_id'],
                item['year'],
                item['left_club_id'],
                item['joined_club_id'],
                item['transfer_fee'],
                item['transfer_type']
            ))

            self.conn.commit()
            return item
        except mysql.connector.Error as e:
            raise DropItem(f'**mySQL error when inserting item: {e}')
