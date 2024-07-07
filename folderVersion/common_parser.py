from enums import MessageField

def add_decimal(value, position):
    return value[:position] + '.' + value[position:]

def parse_message(message, field_lengths, pool_field_lengths=None, decimal_fields=None):
    parsed_message = {}
    start_idx = 0
    num_pools = 0
    # print(field_lengths)
    if decimal_fields is None:
        decimal_fields = {}

    for field, length in field_lengths.items():
        field_value = message[start_idx:start_idx + length]
        print(field)
        if field in decimal_fields:
            position = decimal_fields[field]
            field_value = add_decimal(field_value, position)
        parsed_message[field] = field_value
        # print(field, " ", parsed_message[field])
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

# Test case to run the parser directly
if __name__ == "__main__":
    field_lengths = {
        MessageField.START_MESSAGE_INDICATOR: 1,
        MessageField.MESSAGE_TYPE: 2,
        MessageField.SEQUENCE_NUMBER: 6,
        MessageField.EPN_VERSION_CONTROL: 3,
        MessageField.SUBSCRIBER_ID: 4,
        MessageField.CONNECTION_ID: 4,
        MessageField.INTERNAL_ID: 16,
        MessageField.MESSAGE_ID: 11,
        MessageField.ACKNOWLEDGMENT_CODE: 4,
        MessageField.EPN_ACK_TIMESTAMP: 6,
        MessageField.ORIGINAL_SEQUENCE: 6,
        MessageField.END_MESSAGE_INDICATOR: 1
    }

    # Example test message string
    test_message = "*CC0000970020107210734567890abcdefghij0000000000123456ABCDEFGHIJ^"

    decimal_fields = {
        MessageField.EPN_ACK_TIMESTAMP: 4,
        MessageField.ORIGINAL_SEQUENCE: 4
    }

    parsed_message = parse_message(test_message, field_lengths, decimal_fields=decimal_fields)
    print("Parsed Message:")
    for key, value in parsed_message.items():
        if key == 'pools':
            print("  Pools:")
            for i, pool in enumerate(value):
                print(f"    Pool {i + 1}:")
                for pool_key, pool_value in pool.items():
                    print(f"      {pool_key.value}: {pool_value}")
        else:
            print(f"  {key.value}: {value}")
