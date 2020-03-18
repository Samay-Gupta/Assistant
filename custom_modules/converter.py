def convert_temperature(value, convert_from, convert_to):
    value = float(value)
    current_unit = convert_from.strip().lower()[0]
    converted_data = {
        'k': None,
        'c': None,
        'f': None
    }
    if current_unit == 'k':
        converted_data['k'] = value
        converted_data['c'] = converted_data['k'] - 273.15
        converted_data['f'] = converted_data['c'] * 1.8 + 32
    elif current_unit == 'c':
        converted_data['c'] = value
        converted_data['k'] = converted_data['c'] + 273.15
        converted_data['f'] = converted_data['c'] * 1.8 + 32
    elif current_unit == 'f':
        converted_data['f'] = value
        converted_data['c'] = (converted_data['f'] - 32) * (9/5)
        converted_data['k'] = converted_data['c'] + 273.15
    converted_value = converted_data[convert_to.strip().lower()[0]]
    return round(converted_value, 1)
    