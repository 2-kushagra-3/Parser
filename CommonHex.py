class MessageParser:
    def __init__(self):
        self.parsed_messages = []

    def parse_common(self, message):
        # Common fields for all message types
        parsed_message = {
            "Start Message Indicator": "\x02",
            "Message Type": message[1:3],
            "Sequence Number": message[3:9],
            "EPN Version Control": message[9:12]
        }
        return parsed_message

    def parse_AA(self, message):
        parsed_message = self.parse_common(message)
        # Additional fields specific to AA
        parsed_message.update({
            "Internal ID": message[20:36],
            "Message ID": message[36:47],
            "Acknowledgment Code": message[47:51],
            "EPN ACK Time-stamp": message[51:57],
            "Original Sequence": message[57:63],
            "End Message Indicator": "\x03" if len(message) >= 64 else None
        })
        self.parsed_messages.append(parsed_message)

    def parse_TX(self, message):
        parsed_message = self.parse_common(message)
        # Additional fields specific to TX
        parsed_message.update({
            "TEXT TYPE": message[20:22],
            "MESSAGE TEXT": message[22:152],
            "End Message Indicator": "\x03"
        })
        self.parsed_messages.append(parsed_message)

    def parse_default(self, message):
        parsed_message = self.parse_common(message)
        # Additional fields for default parsing
        parsed_message.update({
            "Additional Field 1": message[20:30],
            "Additional Field 2": message[30:40],
            "End Message Indicator": "\x03"
        })
        self.parsed_messages.append(parsed_message)

    def parse_string(self, input_string):
        current_message = ""
        in_message = False

        i = 0
        while i < len(input_string):
            if input_string[i] == "\x02" and not in_message:
                in_message = True
                current_message = "\x02"  # Initialize with start indicator
                i += 1  # Move past the start indicator
            elif input_string[i] == "\x03" and in_message:
                in_message = False
                message_type = current_message[1:3]
                if message_type == "AA":
                    self.parse_AA(current_message)
                elif message_type == "TX":
                    self.parse_TX(current_message)
                else:
                    self.parse_default(current_message)
                current_message = ""  # Reset current_message for next message
                i += 1  # Move past the end indicator
            elif in_message:
                current_message += input_string[i]
                i += 1
            else:
                i += 1

# Sample input string
sample_string = (
    "\␂AA00009700201072107                061800016180200152554000034\x03"
    # "\x02TX0000010020107110722START OF BUSINESS DAY 06182024\x03"
    # "\x02ON0000010020107110722\x03"
    # "\x02DK0000010020107110722\x03"
    # "\x02CC0000010020107110722\x03"
    # "\x02CX0000010020107110722\x03"
    # "\x02LS0000010020107110722\x03"
    # "\x02HA0000010020107110722\x03"
    # "\x02TX0000010020107110722\x03"
)

# Initialize the MessageParser
parser = MessageParser()

# Parse the string
parser.parse_string(sample_string)

# Get the parsed messages
parsed_messages = parser.parsed_messages

# Print the parsed messages
for i, message in enumerate(parsed_messages):
    print(f"Message {i+1}: {message}")
