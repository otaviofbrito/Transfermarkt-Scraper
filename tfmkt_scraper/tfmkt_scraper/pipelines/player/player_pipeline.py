from itemadapter import ItemAdapter
from tfmkt_scraper.utils import convert_mv, convert_item_str_to_int
import re
import datetime

class PlayerScraperPipeline:
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
        id_keys = ['id', 'current_club']
        convert_item_str_to_int(adapter=adapter, keys=id_keys)


        # Convert height to cm
        height_keys = ['height']
        for height_key in height_keys:
            value = adapter.get(height_key)
            if value:
                value = value.replace('m', '')
                value = value.replace(',', '')
                value = int(value)
                adapter[height_key] = value


        # Convert birth_date
        # remove age
        date_keys = ['birth_date']
        for date_key in date_keys:
            date = adapter.get(date_key)
            if date:
                date = re.sub(r'\(\d+\)', '', date).strip()
                date = datetime.datetime.strptime(date, '%b %d, %Y').strftime('%Y-%m-%d')
                adapter[date_key] = date


        # Convert death_date
        date_keys = ['death_date']
        for date_key in date_keys:
            date = adapter.get(date_key)
            if date:
                date = re.sub(r'\(\d+\)', '', date).strip()
                date = datetime.datetime.strptime(date, '%d.%m.%Y').strftime('%Y-%m-%d')
                adapter[date_key] = date
        return item
