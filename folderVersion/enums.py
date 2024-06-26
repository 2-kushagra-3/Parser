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
    INTERNAL_ID = "Internal ID"
    MESSAGE_ID = "Message ID"
    ACKNOWLEDGMENT_CODE = "Acknowledgment Code"
    EPN_ACK_TIMESTAMP = "EPN ACK Time-stamp"
    ORIGINAL_SEQUENCE = "Original Sequence"
    END_MESSAGE_INDICATOR = "End Message Indicator"
    TEXT_TYPE = "TEXT TYPE"
    MESSAGE_TEXT = "MESSAGE TEXT"
    PLACEHOLDER = "PLACEHOLDER"
