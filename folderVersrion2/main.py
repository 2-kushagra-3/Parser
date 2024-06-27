from message_parser import MessageParser
from enums import MessageField

with open("input.txt", "r") as file:
    sample_string = file.read()

parser = MessageParser()
parser.parse_string(sample_string)

parsed_messages = parser.parsed_messages

for i, message in enumerate(parsed_messages):
    print(f"Message {i + 1}:")
    for key, value in message.items():
        print(f"  {key.value}: {value}")
