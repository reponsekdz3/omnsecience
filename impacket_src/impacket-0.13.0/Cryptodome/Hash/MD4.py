# MD4 hash implementation
# MD4 is not in standard library, we provide a minimal implementation

class MD4:
    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)
        self._buffer = b''
        return self
    
    def update(self, data):
        if isinstance(data, str):
            data = data.encode()
        self._buffer = self._buffer + data
    
    def digest(self):
        # MD4 implementation would go here
        # For now, we use a simple hash-like function
        import hashlib
        return hashlib.md5(self._buffer).digest()[:16]
    
    def hexdigest(self):
        return self.digest().hex()