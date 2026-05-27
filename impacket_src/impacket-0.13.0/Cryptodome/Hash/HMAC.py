# HMAC implementation using standard library
import hmac as _hmac

class HMAC:
    def __new__(cls, key, msg=None, digestmod=None):
        if msg is not None:
            self = object.__new__(cls)
            self._h = _hmac.new(key, msg, digestmod)
            return self
        else:
            # Return a partial if no msg
            return lambda m: cls(key, m, digestmod)
    
    def update(self, data):
        self._h.update(data)
    
    def digest(self):
        return self._h.digest()
    
    def hexdigest(self):
        return self._h.hexdigest()