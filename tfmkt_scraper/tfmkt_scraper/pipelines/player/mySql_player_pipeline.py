import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem


class MySqlPlayerPipeline:
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
      CREATE TABLE IF NOT EXISTS players(
        id BIGINT NOT NULL PRIMARY KEY,
        url VARCHAR(255) NOT NULL,
        name VARCHAR(255) NOT NULL,
        full_name VARCHAR(255),
        birth_date DATE,
        death_date DATE,
        height INT,
        citizenship_1 VARCHAR(255),
        citizenship_2 VARCHAR(255),
        foot VARCHAR(30),
        agent VARCHAR(255),
        current_club_id VARCHAR(15),
        outfitter VARCHAR(255),
        main_position VARCHAR(255),
        current_mv BIGINT NOT NULL
      );
    """)
        self.conn.commit()

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

    def close_spider(self, spider):
        # close cursor and db connection
        self.cur.close()
        self.conn.close()
