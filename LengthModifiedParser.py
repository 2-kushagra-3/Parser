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

class MessageParser:
    def __init__(self):
        self.parsed_messages = []

        self.parsers = {
            MessageType.AA: self.parse_AA,
            MessageType.TX: self.parse_TX,
            MessageType.ON: self.parse_ON,
            MessageType.DK: self.parse_DK,
            MessageType.CC: self.parse_CC,
            MessageType.CX: self.parse_CX,
            MessageType.LS: self.parse_LS,
            MessageType.HA: self.parse_HA,
            MessageType.DEFAULT: self.parse_default
        }

    def parse_common(self, message):
        start_message_indicator_length = 1
        message_type_length = 2
        sequence_number_length = 6
        epn_version_control_length = 3
        subscriber_id_length = 4
        connection_id_length = 4

        common_fields = {
            MessageField.START_MESSAGE_INDICATOR: message[:start_message_indicator_length],
            MessageField.MESSAGE_TYPE: message[start_message_indicator_length:start_message_indicator_length+message_type_length],
            MessageField.SEQUENCE_NUMBER: message[start_message_indicator_length+message_type_length:start_message_indicator_length+message_type_length+sequence_number_length],
            MessageField.EPN_VERSION_CONTROL: message[start_message_indicator_length+message_type_length+sequence_number_length:start_message_indicator_length+message_type_length+sequence_number_length+epn_version_control_length],
            MessageField.SUBSCRIBER_ID: message[start_message_indicator_length+message_type_length+sequence_number_length+epn_version_control_length:start_message_indicator_length+message_type_length+sequence_number_length+epn_version_control_length+subscriber_id_length],
            MessageField.CONNECTION_ID: message[start_message_indicator_length+message_type_length+sequence_number_length+epn_version_control_length+subscriber_id_length:start_message_indicator_length+message_type_length+sequence_number_length+epn_version_control_length+subscriber_id_length+connection_id_length],
        }
        return common_fields

    def parse_AA(self, message):
        parsed_message = self.parse_common(message)
        internal_id_length = 16
        message_id_length = 11
        acknowledgment_code_length = 4
        epn_ack_timestamp_length = 6
        original_sequence_length = 6

        start = 20
        parsed_message.update({
            MessageField.INTERNAL_ID: message[start:start+internal_id_length],
            MessageField.MESSAGE_ID: message[start+internal_id_length:start+internal_id_length+message_id_length],
            MessageField.ACKNOWLEDGMENT_CODE: message[start+internal_id_length+message_id_length:start+internal_id_length+message_id_length+acknowledgment_code_length],
            MessageField.EPN_ACK_TIMESTAMP: message[start+internal_id_length+message_id_length+acknowledgment_code_length:start+internal_id_length+message_id_length+acknowledgment_code_length+epn_ack_timestamp_length],
            MessageField.ORIGINAL_SEQUENCE: message[start+internal_id_length+message_id_length+acknowledgment_code_length+epn_ack_timestamp_length:start+internal_id_length+message_id_length+acknowledgment_code_length+epn_ack_timestamp_length+original_sequence_length],
            MessageField.END_MESSAGE_INDICATOR: "^C"
        })
        self.parsed_messages.append(parsed_message)

    def parse_TX(self, message):
        parsed_message = self.parse_common(message)
        text_type_length = 2
        message_text_length = 130

        start = 20
        parsed_message.update({
            MessageField.TEXT_TYPE: message[start:start+text_type_length],
            MessageField.MESSAGE_TEXT: message[start+text_type_length:start+text_type_length+message_text_length],
            MessageField.END_MESSAGE_INDICATOR: "^C"
        })
        self.parsed_messages.append(parsed_message)

    def parse_ON(self, message):
        parsed_message = self.parse_common(message)

        self.parsed_messages.append(parsed_message)

    def parse_DK(self, message):
        parsed_message = self.parse_common(message)


    def parse_CC(self, message):
        parsed_message = self.parse_common(message)

        self.parsed_messages.append(parsed_message)

    def parse_CX(self, message):
        parsed_message = self.parse_common(message)

        self.parsed_messages.append(parsed_message)

    def parse_LS(self, message):
        parsed_message = self.parse_common(message)

        self.parsed_messages.append(parsed_message)

    def parse_HA(self, message):
        parsed_message = self.parse_common(message)

        self.parsed_messages.append(parsed_message)

    def parse_default(self, message):
        parsed_message = self.parse_common(message)

        self.parsed_messages.append(parsed_message)

    def parse_string(self, input_string):
        current_message = ""
        in_message = False

        for i in range(len(input_string) - 1):
            if input_string[i:i+2] == "^B" and not in_message:
                in_message = True
                current_message = ""
            elif input_string[i:i+2] == "^C" and in_message:
                in_message = False
                message_type = MessageType(current_message[1:3]) if current_message[1:3] in MessageType._value2member_map_ else MessageType.DEFAULT
                parser_function = self.parsers.get(message_type, self.parse_default)
                parser_function(current_message)
            elif in_message:
                current_message += input_string[i]


sample_string = """^BAA00009700201072107                061800016180200152554000034^C
^BTX0000010020107110722START OF BUSINESS DAY 06182024^C"""

parser = MessageParser()

parser.parse_string(sample_string)

parsed_messages = parser.parsed_messages

for i, message in enumerate(parsed_messages):
    formatted_message = {field.name: value for field, value in message.items()}
    print(f"Message {i+1}: {formatted_message}")