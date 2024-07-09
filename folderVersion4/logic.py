import os
from config import MessageField, MessageType, COMMON_FIELD_LENGTHS, SPECIFIC_FIELD_LENGTHS, POOL_FIELD_LENGTHS, DECIMAL_FIELDS

def add_decimal(value, position):
    return value[:position] + '.' + value[position:]

def parse_message(message, field_lengths, pool_field_lengths=None, decimal_fields=None):
    parsed_message = {}
    start_idx = 0
    num_pools = 0

    if decimal_fields is None:
        decimal_fields = {}

    for field, length in field_lengths.items():
        field_value = message[start_idx:start_idx + length]
        if field in decimal_fields:
            position = decimal_fields[field]
            field_value = add_decimal(field_value, position)
        parsed_message[field] = field_value
        if field == MessageField.NUMBER_OF_POOLS:
            num_pools = int(field_value)
        start_idx += length

    if pool_field_lengths and num_pools > 0:
        pools = []
        for _ in range(num_pools):
            pool = {}
            for pool_field, pool_length in pool_field_lengths.items():
                pool_field_value = message[start_idx:start_idx + pool_length]
                if pool_field in decimal_fields:
                    position = decimal_fields[pool_field]
                    pool_field_value = add_decimal(pool_field_value, position)
                pool[pool_field] = pool_field_value
                start_idx += pool_length
            pools.append(pool)
        parsed_message['pools'] = pools

    parsed_message[MessageField.END_MESSAGE_INDICATOR] = message[start_idx:]
    return parsed_message

class MessageParser:
    def __init__(self):
        self.parsed_messages = []
        self.parsers = {
            "AA": self.parse_AA,
            "CC": self.parse_CC,
            # Add other parsers here if needed
            "DEFAULT": self.parse_default
        }

    def parse_string(self, input_string):
        current_message = ""
        in_message = False        
        for char in input_string:
            if char == "*":
                in_message = True
                current_message = ""
            elif char == "^" and in_message:
                in_message = False
                message_type = current_message[0:2]
                current_message = "*" + current_message + "^"
                parser = self.parsers.get(message_type, self.parsers["DEFAULT"])
                parser(current_message)
            elif in_message:
                current_message += char

    def parse_AA(self, message):
        field_lengths = {**COMMON_FIELD_LENGTHS, **SPECIFIC_FIELD_LENGTHS["AA"]}
        decimal_fields = DECIMAL_FIELDS["AA"]
        parsed_message = parse_message(message, field_lengths, None, decimal_fields)
        self.parsed_messages.append(parsed_message)

    def parse_CC(self, message):
        field_lengths = {**COMMON_FIELD_LENGTHS, **SPECIFIC_FIELD_LENGTHS["CC"]}
        pool_field_lengths = POOL_FIELD_LENGTHS["CC"]
        decimal_fields = DECIMAL_FIELDS["CC"]
        parsed_message = parse_message(message, field_lengths, pool_field_lengths, decimal_fields)
        self.parsed_messages.append(parsed_message)

    def parse_default(self, message):
        field_lengths = COMMON_FIELD_LENGTHS
        parsed_message = parse_message(message, field_lengths)
        self.parsed_messages.append(parsed_message)

def main():
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
            for key, value in message.items():
                if key == 'pools':
                    print("  Pools:")
                    for j, pool in enumerate(value):
                        print(f"    Pool {j + 1}:")
                        for pool_key, pool_value in pool.items():
                            print(f"      {pool_key.value}: {pool_value}")
                else:
                    print(f"  {key.value}: {value}")

if __name__ == "__main__":
    main()
