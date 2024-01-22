from itemadapter import ItemAdapter
from tfmkt_scraper.utils import convert_mv, convert_item_str_to_int

class TransferScraperPipeline:
  def process_item(self, item, spider):
    
    adapter =ItemAdapter(item)
    
    #Convert values to int
    str_keys = ['joined_club_id', 'left_club_id', 'player_id', 'year']
    convert_item_str_to_int(adapter=adapter, keys=str_keys)
    
    #Convert transfer fee
    fee_keys = ['transfer_fee']
    for key in fee_keys:
      value = adapter.get(key)
      if isinstance(value, str):
         value = value.replace('€', '')
         adapter[key] = convert_mv(value)
    
    return item