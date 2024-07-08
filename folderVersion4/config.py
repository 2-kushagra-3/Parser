from enum import Enum

class MessageType(Enum):
    AA = "AA"
    TX = "TX"
    ON = "ON"
    DK = "DK"
    CC = "CC"
    CX = "CX"
    LS = "LS"
    HA = "HA"
    DEFAULT = "DEFAULT"

class MessageField(Enum):
    START_MESSAGE_INDICATOR = "Start Message Indicator"
    MESSAGE_TYPE = "Message Type"
    SEQUENCE_NUMBER = "Sequence Number"
    EPN_VERSION_CONTROL = "EPN Version Control"
    SUBSCRIBER_ID = "Subscriber ID"
    CONNECTION_ID = "Connection ID"
    FIELD_7 = "Field 7"
    FIELD_8 = "Field 8"
    NUMBER_OF_POOLS = "Number of Pools"
    FIELD_10 = "Field 10"
    POOL_FIELD_1 = "Pool Field 1"
    POOL_FIELD_2 = "Pool Field 2"
    INTERNAL_ID = "Internal ID"
    MESSAGE_ID = "Message ID"
    ACKNOWLEDGMENT_CODE = "Acknowledgment Code"
    EPN_ACK_TIMESTAMP = "EPN Ack Timestamp"
    ORIGINAL_SEQUENCE = "Original Sequence"
    END_MESSAGE_INDICATOR = "End Message Indicator"

COMMON_FIELD_LENGTHS = {
    MessageField.START_MESSAGE_INDICATOR: 1,
    MessageField.MESSAGE_TYPE: 2,
    MessageField.SEQUENCE_NUMBER: 6,
    MessageField.EPN_VERSION_CONTROL: 3,
    MessageField.SUBSCRIBER_ID: 4,
    MessageField.CONNECTION_ID: 4
}

SPECIFIC_FIELD_LENGTHS = {
    "AA": {
        MessageField.INTERNAL_ID: 16,
        MessageField.MESSAGE_ID: 11,
        MessageField.ACKNOWLEDGMENT_CODE: 4,
        MessageField.EPN_ACK_TIMESTAMP: 6,
        MessageField.ORIGINAL_SEQUENCE: 5,
        MessageField.END_MESSAGE_INDICATOR: 1
    },
    "CC": {
        MessageField.FIELD_7: 10,
        MessageField.FIELD_8: 10,
        MessageField.NUMBER_OF_POOLS: 2,
        MessageField.FIELD_10: 12,
    }
}

POOL_FIELD_LENGTHS = {
    "CC": {
        MessageField.POOL_FIELD_1: 10,
        MessageField.POOL_FIELD_2: 10
    }
}

DECIMAL_FIELDS = {
    "AA": {
        MessageField.ORIGINAL_SEQUENCE: 4,
        MessageField.EPN_ACK_TIMESTAMP: 4
    },
    "CC": {
        MessageField.FIELD_8: 9,
        MessageField.FIELD_10: 10
    }
}
