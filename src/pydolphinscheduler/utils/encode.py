import hashlib


def md5(string: str) -> str:
    """Encode string with MD5 hashlib."""
    return hashlib.md5(string.encode('utf-8')).hexdigest()
