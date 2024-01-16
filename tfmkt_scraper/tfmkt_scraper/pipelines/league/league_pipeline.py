from itemadapter import ItemAdapter

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
            if 'k' in value:
                value = value.replace('k', '')
                value = float(value)
                value = value*1000
            elif 'm' in value:
                value = value.replace('m', '')
                value = float(value)
                value = value*1000000
            elif 'bn' in value:
                value = value.replace('bn', '')
                value = float(value)
                value = value*1000000000
            else:
                value = float(0)
            adapter[mv_key] = value

        return item
