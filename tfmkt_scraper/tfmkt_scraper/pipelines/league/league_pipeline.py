from itemadapter import ItemAdapter
from tfmkt_scraper.utils import convert_mv

class LeagueScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        ##Strip the whitespaces
        field_names = adapter.field_names()
        for field_name in field_names:
            value = adapter.get(field_name)
            adapter[field_name] = value.strip()

        ##Convert current market value to float
        mv_keys = ['league_current_mv']
        for mv_key in mv_keys:
            value = adapter.get(mv_key)
            value = value.replace('€', '')
            convert_mv(value=value)
            adapter[mv_key] = value

        return item
