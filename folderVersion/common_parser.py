from enums import MessageField

def parse_common(message, fields_length):
    parsed_message = {}
    start_idx = 0
    for field, length in fields_length.items():
        parsed_message[field] = message[start_idx:start_idx + length]
        start_idx += length
    return parsed_message, start_idx
