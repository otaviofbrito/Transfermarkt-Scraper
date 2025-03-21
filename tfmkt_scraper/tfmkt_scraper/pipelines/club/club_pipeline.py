from itemadapter import ItemAdapter
from tfmkt_scraper.utils import *


class ClubScrapperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        strip_fields(adapter=adapter)

        # Convert market value
        adapter['current_mv'] = convert_market_value(value=adapter.get('current_mv'))

        # Convert club ID to int
        id_keys = ['id']
        convert_item_str_to_int(adapter=adapter, keys=id_keys)

        convert_empty_strings_to_none(adapter=adapter)

        return item
