# PBKDF2 implementation using standard library
import hashlib
import os

def PBKDF2(password, salt, dkLen=32, count=1000, prf=None):
    """
    PBKDF2 (Password-Based Key Derivation Function 2)
    Uses hashlib.pbkdf2_hmac as fallback
    """
    if prf is None:
        prf = hashlib.sha1
    # Map hash name to hashlib
    if prf == hashlib.sha1 or prf == 'sha1':
        return hashlib.pbkdf2_hmac('sha1', password, salt, count, dkLen)
    elif prf == hashlib.sha256 or prf == 'sha256':
        return hashlib.pbkdf2_hmac('sha256', password, salt, count, dkLen)
    elif prf == hashlib.md5 or prf == 'md5':
        return hashlib.pbkdf2_hmac('md5', password, salt, count, dkLen)
    else:
        # Try to get hash name
        if hasattr(prf, '__name__'):
            return hashlib.pbkdf2_hmac(prf.__name__, password, salt, count, dkLen)
        return hashlib.pbkdf2_hmac('sha1', password, salt, count, dkLen)