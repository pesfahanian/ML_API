import secrets
from passlib.hash import pbkdf2_sha256 as sha256

from settings import SALT_LENGTH


def make_salt():
    """
    Returns a salt string with length 2 * SALT_LENGTH.
    """
    return secrets.token_hex(SALT_LENGTH)


def make_hash(raw):
    """
    Returns the SHA256-hash of an input string.
    """
    return sha256.hash(raw)


def verify_hash(stringed, hashed):
    """
    Verifies the SHA256-hash of an input string against a SHA256-hash.
    """
    if sha256.verify(stringed, hashed):
        return True
    else:
        return False
