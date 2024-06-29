from enums import MessageField

def parse_common(message, field_lengths):
    parsed_message = {}
    start_index = 0
    
    for field, length in field_lengths.items():
        parsed_message[field] = message[start_index:start_index + length].strip()
        start_index += length
    
    return parsed_message