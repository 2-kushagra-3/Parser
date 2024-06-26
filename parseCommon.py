class MessageParser:
    def __init__(self):
        self.parsed_messages = []

    def parse_default(self, message):
        parsed_message = self.parse_common(message)
        parsed_message.update({
            "Additional Field 1": message[20:30],
            "Additional Field 2": message[30:40],
            "End Message Indicator": "^C"
        })
        self.parsed_messages.append(parsed_message)

    def parse_AA(self, message):
        parsed_message = self.parse_common(message)
        parsed_message.update({
            "Internal ID": message[20:36],
            "Message ID": message[36:47],
            "Acknowledgment Code": message[47:51],
            "EPN ACK Time-stamp": message[51:57],
            "Original Sequence": message[57:63],
            "End Message Indicator": "^C"
        })
        self.parsed_messages.append(parsed_message)

    def parse_TX(self, message):
        parsed_message = self.parse_common(message)
        parsed_message.update({
            "TEXT TYPE" : message[20:22],
            "MESSAGE TEXT" : message[22:152],
            "End Message Indicator": "^C"
        })
        self.parsed_messages.append(parsed_message)

    def parse_default(self, message):
        parsed_message = self.parse_common(message)
        parsed_message.update({
            "Additional Field 1": message[20:30],
            "Additional Field 2": message[30:40],
            "End Message Indicator": "^C"
        })
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
                message_type = current_message[1:3]
                if message_type == "AA":
                    self.parse_AA(current_message)
                elif message_type == "TX":
                    self.parse_TX(current_message)
                else:
                    self.parse_default(current_message)
            elif in_message:
                current_message += input_string[i]

sample_string = """^BAA00009700201072107                061800016180200152554000034^C
^BTX0000010020107110722START OF BUSINESS DAY 06182024^C
^BON0000010020107110722^C
^BDK0000010020107110722^C
^BCC0000010020107110722^C
^BCX0000010020107110722^C
^BLS0000010020107110722^C
^BHA0000010020107110722^C
^BTX0000010020107110722^C"""

parser = MessageParser()
parser.parse_string(sample_string)
parsed_messages = parser.parsed_messages

for i, message in enumerate(parsed_messages):
    print(f"Message {i+1}: {message}")
