# ARC4 cipher implementation (compatible with Cryptodome API)
class ARC4:
    def __init__(self, key):
        self.key = key if isinstance(key, bytes) else key.encode() if isinstance(key, str) else bytes(key)
        self.state = list(range(256))
        j = 0
        k = self.key
        for i in range(256):
            j = (j + self.state[i] + k[i % len(k)]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]
        self.i = self.j = 0

    def encrypt(self, data):
        out = bytearray()
        d = data if isinstance(data, bytes) else data.encode() if isinstance(data, str) else bytes(data)
        for n in range(len(d)):
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.state[self.i]) % 256
            self.state[self.i], self.state[self.j] = self.state[self.j], self.state[self.i]
            out.append(d[n] ^ self.state[(self.state[self.i] + self.state[self.j]) % 256])
        return bytes(out)

    def decrypt(self, data):
        return self.encrypt(data)