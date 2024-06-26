from enums import MessageField
from common_parser import parse_common

def parse_AA(message, parsed_messages):
    parsed_message = parse_common(message)
    internal_id_length = 16
    message_id_length = 11
    acknowledgment_code_length = 4
    epn_ack_timestamp_length = 6
    original_sequence_length = 6

    start = 20
    parsed_message.update({
        MessageField.INTERNAL_ID: message[start:start + internal_id_length],
        MessageField.MESSAGE_ID: message[start + internal_id_length:start + internal_id_length + message_id_length],
        MessageField.ACKNOWLEDGMENT_CODE: message[start + internal_id_length + message_id_length:start + internal_id_length + message_id_length + acknowledgment_code_length],
        MessageField.EPN_ACK_TIMESTAMP: message[start + internal_id_length + message_id_length + acknowledgment_code_length:start + internal_id_length + message_id_length + acknowledgment_code_length + epn_ack_timestamp_length],
        MessageField.ORIGINAL_SEQUENCE: message[start + internal_id_length + message_id_length + acknowledgment_code_length + epn_ack_timestamp_length:start + internal_id_length + message_id_length + acknowledgment_code_length + epn_ack_timestamp_length + original_sequence_length],
        MessageField.END_MESSAGE_INDICATOR: "^C"
    })
    parsed_messages.append(parsed_message)

def parse_TX(message, parsed_messages):
    parsed_message = parse_common(message)
    text_type_length = 2
    message_text_length = 130  # Assuming maximum length of message text is 130

    start = 20
    parsed_message.update({
        MessageField.TEXT_TYPE: message[start:start + text_type_length],
        MessageField.MESSAGE_TEXT: message[start + text_type_length:start + text_type_length + message_text_length],
        MessageField.END_MESSAGE_INDICATOR: "^C"
    })
    parsed_messages.append(parsed_message)

def parse_ON(message, parsed_messages):
    parsed_message = parse_common(message)
    # Placeholder parser for ON message type
    parsed_messages.append(parsed_message)

def parse_DK(message, parsed_messages):
    parsed_message = parse_common(message)
    # Placeholder parser for DK message type
    parsed_messages.append(parsed_message)

def parse_CC(message, parsed_messages):
    parsed_message = parse_common(message)
    # Placeholder parser for CC message type
    parsed_messages.append(parsed_message)

def parse_CX(message, parsed_messages):
    parsed_message = parse_common(message)
    # Placeholder parser for CX message type
    parsed_messages.append(parsed_message)

def parse_LS(message, parsed_messages):
    parsed_message = parse_common(message)
    # Placeholder parser for LS message type
    parsed_messages.append(parsed_message)

def parse_HA(message, parsed_messages):
    parsed_message = parse_common(message)
    # Placeholder parser for HA message type
    parsed_messages.append(parsed_message)

def parse_default(message, parsed_messages):
    parsed_message = parse_common(message)
    # Placeholder parser for unknown message types
    parsed_messages.append(parsed_message)
