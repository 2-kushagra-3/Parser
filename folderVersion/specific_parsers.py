from enums import MessageField, MessageType
from common_parser import parse_common_with_pools

COMMON_FIELD_LENGTHS = {
    MessageField.START_MESSAGE_INDICATOR: 1,
    MessageField.MESSAGE_TYPE: 2,
    MessageField.SEQUENCE_NUMBER: 6,
    MessageField.EPN_VERSION_CONTROL: 3,
    MessageField.SUBSCRIBER_ID: 4,
    MessageField.CONNECTION_ID: 4
}

def parse_AA(message, parsed_messages):
    field_lengths = COMMON_FIELD_LENGTHS.copy()
    field_lengths.update({
        MessageField.INTERNAL_ID: 16,
        MessageField.MESSAGE_ID: 11,
        MessageField.ACKNOWLEDGMENT_CODE: 4,
        MessageField.EPN_ACK_TIMESTAMP: 6,
        MessageField.ORIGINAL_SEQUENCE: 5,
        MessageField.END_MESSAGE_INDICATOR: 1
    })
    parsed_message = parse_common_with_pools(message, field_lengths)
    parsed_messages.append(parsed_message)

def parse_TX(message, parsed_messages):
    parsed_message = parse_common_with_pools(message, COMMON_FIELD_LENGTHS)
    parsed_messages.append(parsed_message)

def parse_ON(message, parsed_messages):
    parsed_message = parse_common_with_pools(message, COMMON_FIELD_LENGTHS)
    parsed_messages.append(parsed_message)

def parse_DK(message, parsed_messages):
    parsed_message = parse_common_with_pools(message, COMMON_FIELD_LENGTHS)
    parsed_messages.append(parsed_message)

def parse_CC(message, parsed_messages):
    field_lengths = COMMON_FIELD_LENGTHS.copy()
    field_lengths.update({
        MessageField.FIELD_7: 10,
        MessageField.FIELD_8: 10,
        MessageField.NUMBER_OF_POOLS: 2,
        MessageField.FIELD_10: 12,
    })
    pool_field_lengths = {
        MessageField.POOL_FIELD_1: 10,
        MessageField.POOL_FIELD_2: 10
    }
    decimal_fields = {
        MessageField.FIELD_8: 9,
        MessageField.FIELD_10: 10
    }
    parsed_message = parse_common_with_pools(message, field_lengths, pool_field_lengths, decimal_fields)
    parsed_messages.append(parsed_message)

def parse_CX(message, parsed_messages):
    parsed_message = parse_common_with_pools(message, COMMON_FIELD_LENGTHS)
    parsed_messages.append(parsed_message)

def parse_LS(message, parsed_messages):
    parsed_message = parse_common_with_pools(message, COMMON_FIELD_LENGTHS)
    parsed_messages.append(parsed_message)

def parse_HA(message, parsed_messages):
    parsed_message = parse_common_with_pools(message, COMMON_FIELD_LENGTHS)
    parsed_messages.append(parsed_message)

def parse_default(message, parsed_messages):
    parsed_message = parse_common_with_pools(message, COMMON_FIELD_LENGTHS)
    parsed_messages.append(parsed_message)
