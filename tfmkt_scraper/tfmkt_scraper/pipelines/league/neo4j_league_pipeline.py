from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jLeaguePipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """             
                  MERGE(l:League {league_id:$id})                
                  ON CREATE SET l.url=$url, l.name=$name, l.current_mv=$mv, l.country=$country
                  ON MATCH SET l.url=$url, l.name=$name, l.current_mv=$mv, l.country=$country

                """, id=item['id'], url=item['url'], name=item['league_name'],
                country=item['league_country'], mv=item['league_current_mv'], database_=self.database)

        except Exception as e:
            raise DropItem(f'**Neo4j error when inserting item: {e}')
