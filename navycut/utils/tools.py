from secrets import choice

def generate_random_secret_key(length):
    """
    Return a securely generated random string.
    The bit length of the returned value can be calculated with the formula:
        log_2(len(allowed_chars)^length)
    For example, with default `allowed_chars` (26+26+10), this gives:
      * length: 12, bit length =~ 71 bits
      * length: 22, bit length =~ 131 bits
    """
    allowed_chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!@#$%^&*+:;><?/][}{'
    return ''.join(choice(allowed_chars) for _ in range(length))

def snake_to_camel(snake_str:str) -> str:
    first, *others = snake_str.split('_')
    return ''.join([first.title(), *map(str.title, others)])