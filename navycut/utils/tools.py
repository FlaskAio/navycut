from secrets import choice
import re
from getpass import getuser

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

def snake_to_camel_case(snake_str:str) -> str:
    """
    convert a snake case string to camel case.
    """
    first, *others = snake_str.split('_')
    return ''.join([first.title(), *map(str.title, others)])

def camel_to_snake_case(camel_str) -> str:
    """
    convert a camel case string to snake case.
    """
    camel_str = re.sub(r"((?<=[a-z0-9])[A-Z]|(?!^)[A-Z](?=[a-z]))", r"_\1", camel_str)
    return camel_str.lower().lstrip("_")

def get_default_username() -> str:
    """
    Return the default username.
    """
    username = getuser()
    return username