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
                     


      );
    """)
    
  def process_item(self, item, spider):

    self.cur.execute("""
      INSERT INTO leagues(url, name, country, current_mv)
      VALUES(%s, %s, %s, %s);

    """, (item['url'], item['league_name'], item['league_country'], item['league_current_mv']))

    self.conn.commit()
    return item
  

  def close_spider(self, spider):
    #close cursor and db connection
    self.cur.close()
    self.conn.close()

  