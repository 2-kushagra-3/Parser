from enums import MessageField

def parse_common(message):
    fields_length = {
        MessageField.START_MESSAGE_INDICATOR: 1,
        MessageField.MESSAGE_TYPE: 2,
        MessageField.SEQUENCE_NUMBER: 6,
        MessageField.EPN_VERSION_CONTROL: 3,
        MessageField.SUBSCRIBER_ID: 4,
        MessageField.CONNECTION_ID: 4
    }
    parsed_message = {}
    start_idx = 0
    for field, length in fields_length.items():
        parsed_message[field] = message[start_idx:start_idx + length]
        start_idx += length
    return parsed_message

def parse_AA(message, parsed_messages):
    parsed_message = parse_common(message)
    fields_length = {
        MessageField.INTERNAL_ID: 16,
        MessageField.MESSAGE_ID: 11,
        MessageField.ACKNOWLEDGMENT_CODE: 4,
        MessageField.EPN_ACK_TIMESTAMP: 6,
        MessageField.ORIGINAL_SEQUENCE: 6,
        MessageField.END_MESSAGE_INDICATOR: 1
    }
    start_idx = sum([1, 2, 6, 3, 4, 4])  # Adjusted based on field lengths
    for field, length in fields_length.items():
        parsed_message[field] = message[start_idx:start_idx + length]
        start_idx += length
    parsed_messages.append(parsed_message)

def parse_TX(message, parsed_messages):
    parsed_message = parse_common(message)
    fields_length = {
        MessageField.TEXT_TYPE: 2,
        MessageField.MESSAGE_TEXT: 130,
        MessageField.END_MESSAGE_INDICATOR: 1
    }
    start_idx = sum([1, 2, 6, 3, 4, 4])  # Adjusted based on field lengths
    for field, length in fields_length.items():
        parsed_message[field] = message[start_idx:start_idx + length]
        start_idx += length
    parsed_messages.append(parsed_message)

def parse_default(message, parsed_messages):
    parsed_message = parse_common(message)
    fields_length = {
        MessageField.ADDITIONAL_FIELD_1: 10,
        MessageField.ADDITIONAL_FIELD_2: 10,
        MessageField.END_MESSAGE_INDICATOR: 1
    }
    start_idx = sum([1, 2, 6, 3, 4, 4])  # Adjusted based on field lengths
    for field, length in fields_length.items():
        parsed_message[field] = message[start_idx:start_idx + length]
        start_idx += length
    parsed_messages.append(parsed_message)
