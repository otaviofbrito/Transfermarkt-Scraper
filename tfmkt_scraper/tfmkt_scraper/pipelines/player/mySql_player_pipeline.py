import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.mySql_connection_pipeline import MySqlConnectionPipeline

class MySqlPlayerPipeline(MySqlConnectionPipeline):

    def process_item(self, item, spider):
        try:
            self.cur.execute("""
      INSERT INTO players(
                              id,
                              url,
                              name,
                              full_name,
                              birth_date,
                              death_date,
                              height,
                              citizenship_1,
                              citizenship_2,
                              foot, agent,
                              current_club_id,
                              outfitter, main_position,
                              current_mv
                        )
      VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
      """, (
                item['id'],
                item['url'],
                item['name'],
                item['full_name'],
                item['birth_date'],
                item['death_date'],
                item['height'],
                item['citizenship_1'],
                item['citizenship_2'],
                item['foot'],
                item['agent'],
                item['current_club'],
                item['outfitter'],
                item['main_position'],
                item['current_mv']
            ))

            self.conn.commit()
            return item
        except mysql.connector.Error as e:
            raise DropItem(f'**mySQL error when inserting item: {e}')
