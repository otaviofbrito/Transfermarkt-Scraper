import mysql.connector

class mySqlLeaguePipeline:
  
  def __init__(self):
    self.conn = mysql.connector.connect(
      host='localhost',
      user='root',
      password='123456',
      database='tfmkt_db'
    )

    #cursor, used to execute commands
    self.cur = self.conn.cursor()

    
    #create league table if none exists
    self.cur.execute("""
      CREATE TABLE IF NOT EXISTS leagues(
        id VARCHAR(15) PRIMARY KEY NOT NULL,
        url VARCHAR(255) NOT NULL,                          
        league_name VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL,
        current_mv DOUBLE
      );
    """)
    
  def process_item(self, item, spider):

    self.cur.execute("""
      INSERT INTO leagues(id, url, league_name, country, current_mv)
      VALUES(%s, %s, %s, %s, %s);

    """, (item['id'],item['url'], item['league_name'], item['league_country'], item['league_current_mv']))

    self.conn.commit()
    return item
  

  def close_spider(self, spider):
    #close cursor and db connection
    self.cur.close()
    self.conn.close()

  