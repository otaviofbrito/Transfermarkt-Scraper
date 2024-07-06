import mysql.connector


class MySqlConnectionPipeline:

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
      CREATE TABLE IF NOT EXISTS leagues(
        id VARCHAR(15) PRIMARY KEY NOT NULL,
        url VARCHAR(255) NOT NULL,                          
        league_name VARCHAR(255) NOT NULL,
        country VARCHAR(255) NOT NULL,
        current_mv BIGINT NOT NULL
      );
    """)
        self.conn.commit()

        # create club_league table if none exists
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

        # create clubs table if none exists
        self.cur.execute("""
      CREATE TABLE IF NOT EXISTS clubs(
        id BIGINT PRIMARY KEY NOT NULL,
        url VARCHAR(255) NOT NULL,                          
        club_name VARCHAR(255) NOT NULL,
        id_current_league VARCHAR(15),
        current_mv BIGINT NOT NULL     
      );
    """)
        self.conn.commit()

        # create players table if none exists
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
        current_club_id BIGINT,
        outfitter VARCHAR(255),
        main_position VARCHAR(255),
        current_mv BIGINT NOT NULL
      );
    """)
        self.conn.commit()

      #Create transfers table if none exists
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



    def close_spider(self, spider):
        # close cursor and db connection
        self.cur.close()
        self.conn.close()
