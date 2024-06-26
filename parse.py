class MessageParser:
    def __init__(self):
        self.parsed_messages = []

    def parse_AA(self, message):
        # Parsing logic for AA combination
        parsed_message = {
            "Start Message Indicator": message[0],
            "Message Type": message[1:3],
            "Sequence Number": message[3:9],
            "EPN Version Control": message[9:12],
            "Subscriber ID": message[12:16],
            "Connection ID": message[16:20],
            "Internal ID": message[20:36],
            "Message ID": message[36:47],
            "Acknowledgment Code": message[47:51],
            "EPN ACK Time-stamp": message[51:57],
            "Original Sequence": message[57:63],
            "End Message Indicator": message[63:64]  # Using ^C as the end message indicator
        }
        self.parsed_messages.append(parsed_message)

    def parse_ON(self, message):
        # Placeholder parsing logic for ON combination
        parsed_message = {"Message": "Parsed ON message"}
        self.parsed_messages.append(parsed_message)

    def parse_DK(self, message):
        # Placeholder parsing logic for DK combination
        parsed_message = {"Message": "Parsed DK message"}
        self.parsed_messages.append(parsed_message)

    def parse_CC(self, message):
        # Placeholder parsing logic for CC combination
        parsed_message = {"Message": "Parsed CC message"}
        self.parsed_messages.append(parsed_message)

    def parse_CX(self, message):
        # Placeholder parsing logic for CX combination
        parsed_message = {"Message": "Parsed CX message"}
        self.parsed_messages.append(parsed_message)

    def parse_LS(self, message):
        # Placeholder parsing logic for LS combination
        parsed_message = {"Message": "Parsed LS message"}
        self.parsed_messages.append(parsed_message)

    def parse_HA(self, message):
        # Placeholder parsing logic for HA combination
        parsed_message = {"Message": "Parsed HA message"}
        self.parsed_messages.append(parsed_message)

    def parse_TX(self, message):
        # Placeholder parsing logic for TX combination
        parsed_message = {"Start Message Indicator": message[0],
            "Message Type": message[1:3],
            "Sequence Number": message[3:9],
            "EPN Version Control": message[9:12],
            "Subscriber ID": message[12:16],
            "Connection ID": message[16:20]
            ,"TEXT TYPE" : message[20:22],
            "MESSAGE TEXT" : message[22:152],
            "End Message Indicator": "^C"
        }
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
                elif message_type == "ON":
                    self.parse_ON(current_message)
                elif message_type == "DK":
                    self.parse_DK(current_message)
                elif message_type == "CC":
                    self.parse_CC(current_message)
                elif message_type == "CX":
                    self.parse_CX(current_message)
                elif message_type == "LS":
                    self.parse_LS(current_message)
                elif message_type == "HA":
                    self.parse_HA(current_message)
                elif message_type == "TX":
                    self.parse_TX(current_message)
            elif in_message:
                current_message += input_string[i]

# Sample input string
sample_string = """^BTX0000010020107110722START OF BUSINESS DAY 06182024^C"""
# """^BAA00009700201072107                061800016180200152554000034^C
# ^BLS0000010020107110722^C
# ^BON0000010020107110722^C
# ^BDK0000010020107110722^C
# ^BCC0000010020107110722^C
# ^BCX0000010020107110722^C
# ^BHA0000010020107110722^C
# ^BTX0000010020107110722^C
# ^BAA00009700201072107                061800016180200152554000034^C"""

# Initialize the MessageParser
parser = MessageParser()

# Parse the string
parser.parse_string(sample_string)

# Get the parsed messages
parsed_messages = parser.parsed_messages

# Print the parsed messages
for i, message in enumerate(parsed_messages):
    print(f"Message {i+1}: {message}")
