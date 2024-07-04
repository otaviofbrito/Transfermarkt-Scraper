from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jPlayerPipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """             
                  MERGE(p:Player {player_id:$id})                
                  ON CREATE SET url:$url, name:$name, fullname:$fullname, birthdate:$birthdate,
                    deathdate:$deathdate, height:$height, citizenship_1:$c1, citizenship_2:$c2,
                    foot:$foot, agent:$agent, current_club:$current_club, outfitter:$outfitter,
                    main_position:$main_position, current_mv:$mv

                  ON MATCH SET url:$url, name:$name, fullname:$fullname, birthdate:$birthdate,
                    deathdate:$deathdate, height:$height, citizenship_1:$c1, citizenship_2:$c2,
                    foot:$foot, agent:$agent, current_club:$current_club, outfitter:$outfitter,
                    main_position:$main_position, current_mv:$mv

                """,
                id=item['id'],
                url=item['url'],
                name=item['name'],
                fullname=item['full_name'],
                birthdate=item['birth_date'],
                deathdate=item['death_date'],
                height=item['height'],
                c1=item['citizenship_1'],
                c2=item['citizenship_2'],
                foot=item['foot'],
                agent=item['agent'],
                current_club=item['current_club'],
                outfitter=item['outfitter'],
                main_position=item['main_position'],
                mv=item['current_mv'],
                database_=self.database)

        except Exception as e:
            raise DropItem(f'**Neo4j error when inserting item: {e}')
