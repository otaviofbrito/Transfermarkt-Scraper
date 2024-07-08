from itemadapter import ItemAdapter
from tfmkt_scraper.utils import *


class ClubLeagueScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Convert current market value to float
        value = adapter.get('market_value')
        if value:
            value = value.replace('€', '')
            value = convert_mv(value=value)
            adapter['market_value'] = value
        else:
            adapter['market_value'] = 0

        # Convert league ID to int
        club_id_keys = ['club_id']
        convert_item_str_to_int(adapter=adapter, keys=club_id_keys)

        # Convert squad number to int
        value = adapter.get('squad')
        if value:
            adapter['squad'] = int(value)
        else:
            adapter['squad'] = 0

        # Convert season to int
        season_keys = ['season']
        convert_item_str_to_int(adapter=adapter, keys=season_keys)

        convert_emptystring_to_none(adapter=adapter)

        return item
