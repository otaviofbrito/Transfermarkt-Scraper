from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jTransferPipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """             
                  MERGE(p:Player {player_id:$player_id}) 
                  MERGE(cl:Club {club_left_id:$club_left_id})    
                  MERGE(c2:Club {club_joined_id:$club_joined_id})    

                  MERGE(t:Transfer)
                  ON CREATE SET t.year=$year, t.fee=$fee, t.type=$type
                  ON MATCH SET t.year=$year, t.fee=$fee, t.type=$type

                  MERGE(c1)<-[:LEFT]-(t)-[:JOINED]->(c2)
                  MERGE(t)-[:OF_PLAYER]->(p)
                """, club_id=item['id'], url=item['url'], name=item['club_name'],
                current_league=item['current_league'], mv=item['current_mv'], database_=self.database)

        except Exception as e:
            raise DropItem(f'**Neo4j error when inserting item: {e}')
