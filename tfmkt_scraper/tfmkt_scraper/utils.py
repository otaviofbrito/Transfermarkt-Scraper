def convert_mv(value) -> float:
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

    return value
