import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem


class MySqlTransferPipeline:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            host=crawler.settings.get('MYSQL_HOST'),
            user=crawler.settings.get('MYSQL_USER'),
            password=crawler.settings.get('MYSQL_PASSWORD'),
            database=crawler.settings.get('MYSQL_DATABASE'),
        )

    def open_spider(self, spider):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database
        )

        # cursor, used to execute commands
        self.cur = self.conn.cursor()

        # create league table if none exists
        self.cur.execute("""
      CREATE TABLE IF NOT EXISTS transfers(
        player_id BIGINT NOT NULL,
        year INT NOT NULL,
        left_club_id BIGINT,
        joined_club_id BIGINT,
        transfer_fee BIGINT,
        transfer_type TINYINT NOT NULL,
        PRIMARY KEY(player_id, year, left_club_id, joined_club_id)
      );
    """)
        self.conn.commit()

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

    def close_spider(self, spider):
        # close cursor and db connection
        self.cur.close()
        self.conn.close()
