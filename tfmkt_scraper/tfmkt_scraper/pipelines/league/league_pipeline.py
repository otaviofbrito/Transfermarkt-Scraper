from itemadapter import ItemAdapter
from tfmkt_scraper.utils import *


class LeagueScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Strip the whitespaces
        strip_fields(adapter=adapter)

        # Convert current market value to float
        mv_key = 'league_current_mv'
        value = adapter.get(mv_key)
        if value:
            value = value.replace('€', '')
            value = convert_mv(value=value)
            adapter[mv_key] = value
        else:
            adapter[mv_key] = 0

        convert_emptystring_to_none(adapter=adapter)

        return item
