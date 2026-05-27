# AES cipher shim using cryptography library
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class AES:
    def __new__(cls, key, mode, iv=None):
        self = object.__new__(cls)
        self.key = key
        self.mode = mode
        self.iv = iv
        backend = default_backend()
        if mode == 1:  # MODE_ECB
            self._cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
        elif mode == 2:  # MODE_CBC
            if iv is None:
                raise ValueError("CBC mode requires IV")
            self._cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
        else:
            raise ValueError(f"Unsupported mode: {mode}")
        self._encryptor = self._cipher.encryptor()
        self._decryptor = self._cipher.decryptor()
        return self
    
    def encrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        # Pad to 16-byte boundary
        pad_len = 16 - (len(data) % 16)
        data = data + bytes([pad_len] * pad_len)
        return self._encryptor.update(data) + self._encryptor.finalize()
    
    def decrypt(self, data):
        if isinstance(data, str):
            data = data.encode()
        return self._decryptor.update(data) + self._decryptor.finalize()