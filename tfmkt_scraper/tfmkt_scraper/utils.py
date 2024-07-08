from itemadapter import ItemAdapter
import re


def convert_mv(value) -> int:
    if 'k' in value:
        value = value.replace('k', '')
        value = float(value)
        value = int(value*1000)
    elif 'm' in value:
        value = value.replace('m', '')
        value = float(value)
        value = int(value*1000000)
    elif 'bn' in value:
        value = value.replace('bn', '')
        value = float(value)
        value = int(value*1000000000)
    else:
        value = 0

    return value


def convert_item_str_to_int(adapter: ItemAdapter, keys):
    for key in keys:
        value = adapter.get(key)
        if value:
            adapter[key] = int(value)


def get_club_id(url):
    regex_match_id = re.search(r'\/verein\/(\d+)', url, re.IGNORECASE)
    return regex_match_id.group(1)


def get_player_id(url):
    regex_match_payer_id = re.search(
        r'\/profil\/spieler\/(\d+)', url, re.IGNORECASE)
    return regex_match_payer_id.group(1)


def convert_emptystring_to_none(adapter: ItemAdapter):
    field_names = adapter.field_names()
    for field in field_names:
        value = adapter.get(field)
        if value == '':
            adapter[field] = None


def strip_fields(adapter: ItemAdapter):
    field_names = adapter.field_names()
    for field in field_names:
        value = adapter.get(field)
        if value:
            adapter[field] = value.strip()
