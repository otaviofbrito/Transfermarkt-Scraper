from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jClubLeaguePipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """             
                  MERGE(l:League {league_id:$league_id})
                  MERGE(c:Club {club_id:$club_id})                

                  MERGE(c)-[:COMPETED_IN]->(l)
                  WITH c,l, $season AS season
                  CALL apoc.merge.relationship(c, 'COMPETED_IN_' + $season, {},
                    {squad_number:$squad_number, market_value:$mv}, l,
                      {squad_number:$squad_number, market_value:$mv}) YIELD rel
                  RETURN rel
                """, club_id=item['club_id'], league_id=item['league_id'], season=item['season'],
                squad_number=item['squad'], mv=item['market_value'], database_=self.database)
            return item
        except Exception as e:
            raise DropItem(f'**Neo4j error when inserting item: {e}')
