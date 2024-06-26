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

def parse_common(message):
    start_message_indicator_length = 1
    message_type_length = 2
    sequence_number_length = 6
    epn_version_control_length = 3
    subscriber_id_length = 4
    connection_id_length = 4

    common_fields = {
        MessageField.START_MESSAGE_INDICATOR: message[:start_message_indicator_length],
        MessageField.MESSAGE_TYPE: message[start_message_indicator_length:start_message_indicator_length + message_type_length],
        MessageField.SEQUENCE_NUMBER: message[start_message_indicator_length + message_type_length:start_message_indicator_length + message_type_length + sequence_number_length],
        MessageField.EPN_VERSION_CONTROL: message[start_message_indicator_length + message_type_length + sequence_number_length:start_message_indicator_length + message_type_length + sequence_number_length + epn_version_control_length],
        MessageField.SUBSCRIBER_ID: message[start_message_indicator_length + message_type_length + sequence_number_length + epn_version_control_length:start_message_indicator_length + message_type_length + sequence_number_length + epn_version_control_length + subscriber_id_length],
        MessageField.CONNECTION_ID: message[start_message_indicator_length + message_type_length + sequence_number_length + epn_version_control_length + subscriber_id_length:start_message_indicator_length + message_type_length + sequence_number_length + epn_version_control_length + subscriber_id_length + connection_id_length],
    }
    return common_fields

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
        MessageField.END_MESSAGE_INDICATOR: "\x03"  # Hex 03
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
        MessageField.END_MESSAGE_INDICATOR: "\x03"  # Hex 03
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

class MessageParser:
    def __init__(self):
        self.parsed_messages = []

        self.parsers = {
            MessageType.AA: parse_AA,
            MessageType.TX: parse_TX,
            MessageType.ON: parse_ON,
            MessageType.DK: parse_DK,
            MessageType.CC: parse_CC,
            MessageType.CX: parse_CX,
            MessageType.LS: parse_LS,
            MessageType.HA: parse_HA,
            MessageType.DEFAULT: parse_default
        }

    def parse_string(self, input_string):
        current_message = ""
        in_message = False

        i = 0
        while i < len(input_string):
            if input_string[i:i + 1] == "\x02" and not in_message:
                in_message = True
                current_message = ""
                i += 1  # Move past the start indicator
            elif input_string[i:i + 1] == "\x03" and in_message:
                in_message = False
                message_type = current_message[1:3]
                parser = self.parsers.get(MessageType(message_type), self.parsers[MessageType.DEFAULT])
                parser(current_message + "\x03", self.parsed_messages)  # Adding "\x03" as the end of the message (Hex 03)
                i += 1  # Move past the end indicator
            elif in_message:
                current_message += input_string[i]
                i += 1
            else:
                i += 1

# Sample input string
sample_string = "\x02AA00009700201072107                061800016180200152554000034\x03"

# Initialize the MessageParser
parser = MessageParser()

# Parse the string
parser.parse_string(sample_string)

# Get the parsed messages
parsed_messages = parser.parsed_messages

# Print the parsed messages
for i, message in enumerate(parsed_messages):
    print(f"Message {i+1}: {message}")
