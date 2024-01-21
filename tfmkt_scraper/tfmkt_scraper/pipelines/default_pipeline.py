# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from tfmkt_scraper.utils import convert_mv, convert_item_str_to_int

class TfmktScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        field_names = adapter.field_names()
        for field in field_names:
            value = adapter.get(field)
            if value:
                adapter[field] = value.strip()

        # Convert market value
        mv_keys = ['current_mv']
        for mv_key in mv_keys:
            value = adapter.get(mv_key)
            if value:
                adapter[mv_key] = convert_mv(value=value)
            else:
                adapter[mv_key] = 0

        # Convert club ID to int
        id_keys = ['id']
        convert_item_str_to_int(adapter=adapter, keys=id_keys)

        return item
