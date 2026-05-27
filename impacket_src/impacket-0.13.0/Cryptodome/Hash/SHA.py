# SHA hash implementation using standard library
import hashlib

class SHA:
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self._h = hashlib.sha1()
        return self
    
    def update(self, data):
        self._h.update(data if isinstance(data, bytes) else data.encode() if isinstance(data, str) else bytes(data))
    
    def digest(self):
        return self._h.digest()
    
    def hexdigest(self):
        return self._h.hexdigest()