from enums import MessageField

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