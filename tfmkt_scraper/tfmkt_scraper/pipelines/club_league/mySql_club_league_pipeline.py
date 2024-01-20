import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem

class MySqlClub_LeaguePipeline:
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

    #cursor, used to execute commands
    self.cur = self.conn.cursor()

    #create league table if none exists
    self.cur.execute("""
      CREATE TABLE IF NOT EXISTS club_league(
        club_id BIGINT NOT NULL,
        league_id VARCHAR(15) NOT NULL,
        season INT NOT NULL,
        squad INT,
        market_value BIGINT NOT NULL,
        PRIMARY KEY(club_id, league_id, season)
      );
    """)
    self.conn.commit()

    
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
  

  def close_spider(self, spider):
    #close cursor and db connection
    self.cur.close()
    self.conn.close()
