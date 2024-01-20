from itemadapter import ItemAdapter
from tfmkt_scraper.utils import convert_mv, convert_item_str_to_int


class ClubLeagueScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Convert current market value to float
        mv_keys = ['market_value']
        for mv_key in mv_keys:
            value = adapter.get(mv_key)
            if value:
              value = value.replace('€', '')
              value = convert_mv(value=value)
              adapter[mv_key] = value
            else: adapter[mv_key] = 0
                
            

        ##Convert league ID to int
        club_id_keys = ['club_id']
        convert_item_str_to_int(adapter=adapter, keys=club_id_keys)

        ##Convert squad number to int
        squad_keys = ['squad']
        for key in squad_keys:
            value = adapter.get(key)
            if value:
              adapter[key] = int(value)
            else:
               adapter[key] = 0


        ##Convert season to int
        season_keys = ['season']
        convert_item_str_to_int(adapter=adapter, keys=season_keys)
            

        return item
