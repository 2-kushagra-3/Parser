import os
from config import MessageField, MessageType, COMMON_FIELD_LENGTHS, SPECIFIC_FIELD_LENGTHS, POOL_FIELD_LENGTHS, DECIMAL_FIELDS

def add_decimal(value, position):
    return value[:position] + '.' + value[position:]

def parse_message(message, field_lengths, pool_field_lengths=None, decimal_fields=None):
    start_idx = 0
    num_pools = 0

    if decimal_fields is None:
        decimal_fields = {}

    for field, length in field_lengths.items():
        field_value = message[start_idx:start_idx + length]
        if field in decimal_fields:
            position = decimal_fields[field]
            field_value = add_decimal(field_value, position)
        print(f"{field.value}: {field_value}")
        if field == MessageField.NUMBER_OF_POOLS:
            num_pools = int(field_value)
        start_idx += length

    if pool_field_lengths and num_pools > 0:
        print("Pools:")
        for pool_index in range(num_pools):
            pool = {}
            print(f"  Pool {pool_index + 1}:")
            for pool_field, pool_length in pool_field_lengths.items():
                pool_field_value = message[start_idx:start_idx + pool_length]
                if pool_field in decimal_fields:
                    position = decimal_fields[pool_field]
                    pool_field_value = add_decimal(pool_field_value, position)
                print(f"    {pool_field.value}: {pool_field_value}")
                start_idx += pool_length

    print(f"{MessageField.END_MESSAGE_INDICATOR.value}: {message[start_idx:]}")
    return

class MessageParser:
    def __init__(self):
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
        parse_message(message, field_lengths, None, decimal_fields)

    def parse_CC(self, message):
        field_lengths = {**COMMON_FIELD_LENGTHS, **SPECIFIC_FIELD_LENGTHS["CC"]}
        pool_field_lengths = POOL_FIELD_LENGTHS["CC"]
        decimal_fields = DECIMAL_FIELDS["CC"]
        parse_message(message, field_lengths, pool_field_lengths, decimal_fields)

    def parse_default(self, message):
        print("Using default parser")  # Print the message before parsing
        field_lengths = COMMON_FIELD_LENGTHS
        parse_message(message, field_lengths)

def main():
    file_path = r"input.txt"

    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
    else:
        with open(file_path, "r") as file:
            sample_string = file.read()

        parser = MessageParser()
        parser.parse_string(sample_string)

if __name__ == "__main__":
    main()
