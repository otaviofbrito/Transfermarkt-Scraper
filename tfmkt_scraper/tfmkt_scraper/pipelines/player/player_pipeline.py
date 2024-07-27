from itemadapter import ItemAdapter
from tfmkt_scraper.utils import *
import re
import datetime


class PlayerScraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        strip_fields(adapter=adapter)

        # Convert market value
        adapter['current_mv'] = convert_market_value(value=adapter.get('current_mv'))

        # Convert club ID to int
        id_keys = ['id', 'current_club']
        convert_item_str_to_int(adapter=adapter, keys=id_keys)

        # Convert height to cm
        self.convert_height(adapter=adapter)

        # Convert birth_date
        self.convert_date(
            adapter=adapter, date_type='birth_date', date_format='%b %d, %Y')

        # Convert death_date
        self.convert_date(
            adapter=adapter, date_type='death_date', date_format='%d.%m.%Y')

        # Convert empty strings to None | '' -> None
        convert_empty_strings_to_none(adapter=adapter)

        return item

    def convert_height(self, adapter: ItemAdapter) -> None:
        value = adapter.get('height')
        if value:
            try:
                value = value.replace('m', '')
                value = value.replace(',', '')
                value = value.strip()
                value = int(value)
                adapter['height'] = value
            except ValueError as e:
                print(f"Error converting value to integer: {e}")
                adapter['height'] = None

    def convert_date(self, adapter: ItemAdapter, date_type: str, date_format: str) -> None:
        date = adapter.get(date_type)
        if date:
            date = re.sub(r'\([^()]*\)', '', date).strip()
            try:
                date = datetime.datetime.strptime(
                    date, date_format).strftime('%Y-%m-%d')
                adapter[date_type] = date
            except ValueError:
                # If date only contains year, set it to None
                adapter[date_type] = None
