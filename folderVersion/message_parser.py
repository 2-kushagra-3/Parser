from enums import MessageType
from specific_parsers import parse_AA, parse_TX, parse_ON, parse_DK, parse_CC, parse_CX, parse_LS, parse_HA, parse_default

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

        for i in range(len(input_string) - 1):
            if input_string[i:i + 2] == "^B" and not in_message:
                in_message = True
                current_message = ""
            elif input_string[i:i + 2] == "^C" and in_message:
                in_message = False
                message_type = current_message[1:3]
                parser = self.parsers.get(MessageType(message_type), self.parsers[MessageType.DEFAULT])
                parser(current_message + "^C", self.parsed_messages)
            elif in_message:
                current_message += input_string[i]
