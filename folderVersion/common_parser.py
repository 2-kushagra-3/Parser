from enums import MessageField

def add_decimal(value, position):
    return value[:position] + '.' + value[position:]

def parse_common_with_pools(message, field_lengths, pool_field_lengths=None, decimal_fields=None):
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
