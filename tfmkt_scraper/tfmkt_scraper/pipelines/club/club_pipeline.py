from itemadapter import ItemAdapter
from tfmkt_scraper.utils import convert_mv


class ClubScrapperPipeline:
  def process_item(self, item , spider):

    adapter = ItemAdapter(item)

    field_names = adapter.field_names()
    for field_name in field_names:
      value = adapter.get(field_name)
      if value:
        adapter[field_name] = value.strip()

    ##Convert market value
    mv_keys = ['current_mv']
    for mv_key  in mv_keys:
      value = adapter.get(mv_key)
      if value:
        convert_mv(value=value)
        adapter[mv_key] = value
      else:
        adapter[mv_key] = float(0)


    ##Convert club ID to int
    id_keys = ['id']
    for id_key in id_keys:
      id = adapter.get(id_key)
      adapter[id] = int(id)

    return item