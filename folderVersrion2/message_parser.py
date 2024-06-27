from enums import MessageType
from specific_parsers import parse_AA, parse_TX, parse_default

class MessageParser:
    def __init__(self):
        self.parsed_messages = []

    def parse_string(self, input_string):
        current_message = ""
        in_message = False

        i = 0
        while i < len(input_string):
            if input_string[i] == '*':
                in_message = True
                current_message = ""
            elif input_string[i] == '^' and in_message:
                in_message = False
                message_type = current_message[1:3]
                if message_type == MessageType.AA.value:
                    parse_AA(current_message, self.parsed_messages)
                elif message_type == MessageType.TX.value:
                    parse_TX(current_message, self.parsed_messages)
                else:
                    parse_default(current_message, self.parsed_messages)
            elif in_message:
                current_message += input_string[i]
            i += 1
