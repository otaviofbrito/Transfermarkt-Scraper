from scrapy.exceptions import DropItem
from tfmkt_scraper.pipelines.neo4j_connection_pipeline import Neoj4jConnectionPipeline


class Neo4jPlayerPipeline(Neoj4jConnectionPipeline):
    def process_item(self, item, spider):
        try:
            self.driver.execute_query(
                """             
                  MERGE(p:Player {player_id:$id})                
                  ON CREATE SET p.url=$url, p.name=$name, p.fullname=$fullname, p.birthdate=$birthdate,
                    p.deathdate=$deathdate, p.height=$height, p.citizenship_1=$c1, p.citizenship_2=$c2,
                    p.foot=$foot, p.agent=$agent, p.current_club=$current_club, p.outfitter=$outfitter,
                    p.main_position=$main_position, p.current_mv=$mv

                  ON MATCH SET p.url=$url, p.name=$name, p.fullname=$fullname, p.birthdate=$birthdate,
                    p.deathdate=$deathdate, p.height=$height, p.citizenship_1=$c1, p.citizenship_2=$c2,
                    p.foot=$foot, p.agent=$agent, p.current_club=$current_club, p.outfitter=$outfitter,
                    p.main_position=$main_position, p.current_mv=$mv

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
