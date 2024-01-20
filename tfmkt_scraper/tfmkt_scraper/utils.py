from itemadapter import ItemAdapter

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



def convert_item_str_to_int(adapter:ItemAdapter, keys):
    for key in keys:
        value = adapter.get(key)
        if  value: adapter[key] = int(value)
