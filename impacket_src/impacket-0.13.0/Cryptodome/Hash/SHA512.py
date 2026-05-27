# SHA512 hash implementation using standard library
import hashlib

class SHA512:
    """SHA512 hash for SMB3 pre-authentication"""
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self._h = hashlib.sha512()
        return self
    
    def update(self, data):
        self._h.update(data if isinstance(data, bytes) else data.encode() if isinstance(data, str) else bytes(data))
    
    def digest(self):
        return self._h.digest()
    
    def hexdigest(self):
        return self._h.hexdigest()