import secrets
from passlib.hash import pbkdf2_sha256 as sha256

from settings import SALT_LENGTH


def make_salt() -> str:
    """
    [Returns a salt string with length 2 * SALT_LENGTH.]

    Returns:
        str: [Generated salt string.]
    """
    return secrets.token_hex(SALT_LENGTH)


def make_hash(raw: str) -> str:
    """
    [Returns the SHA256 hash of an input string.]

    Args:
        raw (str): [Raw input to be digested.]

    Returns:
        str: [Hash digest of raw input.]
    """
    return sha256.hash(raw)


def verify_hash(stringed: str, hashed: str) -> bool:
    """
    [Verifies the SHA256 hash of an input string against a SHA256-hash.]

    Args:
        stringed (str): [Raw string to verify the digest against.]
        hashed (str): [Hash digest string.]

    Returns:
        bool: [Hash and string match boolean.]
    """
    if sha256.verify(stringed, hashed):
        return True
    else:
        return False
