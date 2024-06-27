# message_parser.py

from enums import MessageType
from specific_parsers import parse_AA, parse_TX, parse_ON, parse_DK, parse_CC, parse_CX, parse_LS, parse_HA, parse_default
import logging

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

        # Configure logging
        logging.basicConfig(level=logging.DEBUG)
        self.logger = logging.getLogger(__name__)

    def parse_string(self, input_string):
        current_message = ""
        in_message = False

        for char in input_string:
            if char == "*":
                in_message = True
                current_message = ""
            elif char == "^" and in_message:
                in_message = False
                if len(current_message) > 20:  # Ensure current_message is valid
                    message_type = current_message[0:2]  # Extract message type
                    self.logger.debug(f"Extracted message_type: {message_type}")
                    
                    try:
                        current_message = "*"+current_message+"^"
                        parsed_type = MessageType(message_type)
                        parser = self.parsers.get(parsed_type, self.parsers[MessageType.DEFAULT])
                        parser(current_message, self.parsed_messages)
                    except ValueError:
                        self.logger.error(f"Invalid message_type: {message_type}")
            elif in_message:
                current_message += char
