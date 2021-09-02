from hashlib import sha256
from ..errors.misc import DataTypeMismatchError

def create_password_hash(password:str) -> str:
    """
    It returns the default hash value of the provided password
    :param password: the password string.
    """
    if not isinstance(password, str): 
        raise DataTypeMismatchError(password, "create_password_hash", "str")
        
    return f"navycut<sha-256>{sha256(password.encode('utf8')).hexdigest()}"

def check_password_hash(db_password, password) -> bool:
    """
    It returns a boolean indicating whether the password hash is correct as per the database or not.
    :param db_password: the password_hash present in the database(example: user.password)
    :param password: the password provided by the user.
    """
    return db_password == create_password_hash(password)