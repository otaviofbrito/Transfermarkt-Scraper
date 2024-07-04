from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jClubPipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """             
                  MERGE(c:Club {club_id:$club_id})                
                  ON CREATE SET url=$url, name=$name, current_mv=$mv, current_league=$current_league
                  ON MATCH SET url=$url, name=$name, current_mv=$mv, current_league=$current_league

                """, club_id=item['id'], url=item['url'], name=item['club_name'],
                current_league=item['current_league'], mv=item['current_mv'], database_=self.database)

        except Exception as e:
            raise DropItem(f'**Neo4j error when inserting item: {e}')
