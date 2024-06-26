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
            "End Message Indicator": message[63]  
        }
        if len(message) >= 64:
            parsed_message["End Message Indicator"] = message[63]
        else:
            parsed_message["End Message Indicator"] = None
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
                if current_message[1:3] == "AA":
                    self.parse_AA(current_message + "^C")  # Adding "^C" to the end of the message
            elif in_message:
                current_message += input_string[i]

# Sample input string
sample_string = """^BAA00009700201072107                061800016180200152554000034^C"""
# ^BTX0000010020107110722START OF BUSINESS DAY 06182024^C
# ^BTX0000010020107110722START OF BUSINESS DAY 06182024
# ^C

# Initialize the MessageParser
parser = MessageParser()

# Parse the string
parser.parse_string(sample_string)

# Get the parsed messages
parsed_messages = parser.parsed_messages

# Print the parsed messages
for i, message in enumerate(parsed_messages):
    print(f"Message {i+1}: {message}")
