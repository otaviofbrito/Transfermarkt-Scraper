import mysql.connector
from mysql.connector import errorcode
from scrapy.exceptions import DropItem

class MySqlClubPipeline:
  
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
      CREATE TABLE IF NOT EXISTS clubs(
        id BIGINT PRIMARY KEY NOT NULL,
        url VARCHAR(255) NOT NULL,                          
        club_name VARCHAR(255) NOT NULL,
        id_current_league VARCHAR(15),
        current_mv DOUBLE NOT NULL     
      );
    """)
    self.conn.commit()

    
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
  

  def close_spider(self, spider):
    #close cursor and db connection
    self.cur.close()
    self.conn.close()

  