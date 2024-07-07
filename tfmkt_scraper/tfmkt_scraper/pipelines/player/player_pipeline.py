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
        value = adapter.get('current_mv')
        if value:
            adapter['current_mv'] = convert_mv(value=value)
        else:
            adapter['current_mv'] = 0

        # Convert club ID to int
        id_keys = ['id', 'current_club']
        convert_item_str_to_int(adapter=adapter, keys=id_keys)

        # Convert height to cm
        value = adapter.get('height')
        if value:
            value = value.replace('m', '')
            value = value.replace(',', '')
            value = int(value)
            adapter['height'] = value

        # Convert birth_date
        # remove age
        date = adapter.get('birth_date')
        if date:
            date = re.sub(r'\([^()]*\)', '', date).strip()
            try:
                date = datetime.datetime.strptime(
                    date, '%b %d, %Y').strftime('%Y-%m-%d')
                adapter['birth_date'] = date
            except ValueError:
                # If date only contains year, set it to None
                adapter['birth_date'] = None

        # Convert death_date
        date = adapter.get('death_date')
        if date:
            date = re.sub(r'\([^()]*\)', '', date).strip()
            try:
                date = datetime.datetime.strptime(
                    date, '%d.%m.%Y').strftime('%Y-%m-%d')
                adapter['death_date'] = date
            except ValueError:
                # If date only contains year, set it to None
                adapter['death_date'] = None

        # Convert empty strings to None | '' -> None
        for field in field_names:
            value = adapter.get(field)
            if value == '':
                adapter[field] = None

        return item
