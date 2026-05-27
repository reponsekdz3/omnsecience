# DES3 cipher shim (placeholder)
class DES3:
    @staticmethod
    def new(key, mode, *args, **kwargs):
        class DES3Cipher:
            def __init__(self, k, m):
                self.key = k
                self.mode = m
            def encrypt(self, data):
                return data
            def decrypt(self, data):
                return data
        return DES3Cipher(key, mode)