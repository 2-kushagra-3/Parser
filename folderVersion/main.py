import os
from message_parser import MessageParser

file_path = r"input.txt"

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
        for key in message:
            if key == 'pools':
                print("  Pools:")
                for j, pool in enumerate(message[key]):
                    print(f"    Pool {j + 1}:")
                    for pool_key in pool:
                        print(f"      {pool_key.value}: {pool[pool_key]}")
            else:
                print(f"  {key.value}: {message[key]}")
