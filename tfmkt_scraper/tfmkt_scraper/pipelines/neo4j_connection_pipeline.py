from neo4j import GraphDatabase


class Neoj4jConnectionPipeline:
    def __init__(self, uri, user, password, database) -> None:
        self.uri = uri
        self.user = user
        self.password = password
        self.database = database

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            uri=crawler.settings.get('NEO4J_URI'),
            user=crawler.settings.get('NEO4J_USER'),
            password=crawler.settings.get('NEO4J_PASSWORD'),
            database=crawler.settings.get('NEO4J_DATABASE')
        )

    def open_spider(self, spider):
        self.driver = GraphDatabase.driver(
            self.uri, auth=(self.user, self.password))
        try:
            self.driver.execute_query(
                "CREATE CONSTRAINT player_id IF NOT EXISTS FOR (p:Player) REQUIRE p.player_id IS UNIQUE", database_=self.database)

            self.driver.execute_query(
                "CREATE CONSTRAINT league_id IF NOT EXISTS FOR (l:League) REQUIRE l.league_id IS UNIQUE", database_=self.database)

            self.driver.execute_query(
                "CREATE CONSTRAINT club_id IF NOT EXISTS FOR (c:Club) REQUIRE c.club_id IS UNIQUE", database_=self.database)

        except Exception as e:
            print(e)

    def close_spider(self, spider):
        self.driver.close()
