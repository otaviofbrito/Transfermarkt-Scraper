from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jTransferPipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """
                  MERGE(p:Player {player_id:$player_id})
                  MERGE(c1:Club {club_id:$club_left_id})
                  MERGE(c2:Club {club_id:$club_joined_id})

                  MERGE(c1)<-[:LEFT]-(t:Transfer {year:$year, fee:$fee, type:$type, player_id:$player_id})-[:JOINED]->(c2)
                  MERGE(t)-[:OF_PLAYER]->(p)
                """,
                player_id=item['player_id'],
                year=item['year'],
                club_left_id=item['left_club_id'],
                club_joined_id=item['joined_club_id'],
                fee=item['transfer_fee'],
                type=item['transfer_type'],
                database_=self.database)
            return item
        except Exception as e:
            raise DropItem(f'**Neo4j error when inserting item: {e}')
