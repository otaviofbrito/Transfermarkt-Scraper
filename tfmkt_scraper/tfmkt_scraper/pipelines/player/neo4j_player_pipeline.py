from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jPlayerPipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """
                  MERGE(p:Player {player_id:$id})
                  ON CREATE SET p.url=$url, p.name=$name, p.fullname=$fullname, p.birthdate=$birthdate,
                    p.deathdate=$deathdate, p.height=$height,p.foot=$foot, p.agent=$agent, p.current_club=$current_club,
                    p.outfitter=$outfitter,p.main_position=$main_position, p.current_mv=$mv
                  ON MATCH SET p.url=$url, p.name=$name, p.fullname=$fullname, p.birthdate=$birthdate,
                    p.deathdate=$deathdate, p.height=$height,p.foot=$foot, p.agent=$agent, p.current_club=$current_club,
                    p.outfitter=$outfitter, p.main_position=$main_position, p.current_mv=$mv
                """,
                id=item['id'],
                url=item['url'],
                name=item['name'],
                fullname=item['full_name'],
                birthdate=item['birth_date'],
                deathdate=item['death_date'],
                height=item['height'],
                foot=item['foot'],
                agent=item['agent'],
                current_club=item['current_club'],
                outfitter=item['outfitter'],
                main_position=item['main_position'],
                mv=item['current_mv'],
                database_=self.database)

            if item['citizenship_1']:
                self.driver.execute_query(
                    """
                    MATCH(p:Player {player_id:$id})
                    MERGE (c:Country {name: toUpper($c1)})
                    MERGE (p)-[:HAS_CITIZENSHIP]->(c)
                    """, id=item['id'], c1=item['citizenship_1'], database_=self.database)

            if item['citizenship_2']:
                self.driver.execute_query(
                    """
                    MATCH(p:Player {player_id:$id})
                    MERGE (c:Country {name: toUpper($c2)})
                    MERGE (p)-[:HAS_CITIZENSHIP]->(c)
                    """, id=item['id'], c2=item['citizenship_2'], database_=self.database)
            return item
        except Exception as e:
            raise DropItem(f'**Neo4j error when inserting item: {e}')
