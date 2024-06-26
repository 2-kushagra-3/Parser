import os
from message_parser import MessageParser
from enums import MessageField

file_path = r"input.txt"

# Check if the file exists
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
else:

    with open(file_path, "r") as file:
        sample_string = file.read()

    parser = MessageParser()

    parser.parse_string(sample_string)

    parsed_messages = parser.parsed_messages

    for i, message in enumerate(parsed_messages):
        print(f"Message {i + 1}:")
        for key, value in message.items():
            print(f"  {key.value}: {value}")
