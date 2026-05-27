
# ARC4 cipher shim for impacket compatibility
class ARC4:
    def __init__(self, key):
        self.key = key
        self.state = list(range(256))
        j = 0
        k = key
        for i in range(256):
            j = (j + self.state[i] + k[i % len(k)]) % 256
            self.state[i], self.state[j] = self.state[j], self.state[i]
        self.i = self.j = 0

    def encrypt(self, data):
        out = bytearray()
        for n in range(len(data)):
            self.i = (self.i + 1) % 256
            self.j = (self.j + self.state[self.i]) % 256
            self.state[self.i], self.state[self.j] = self.state[self.j], self.state[self.i]
            out.append(data[n] ^ self.state[(self.state[self.i] + self.state[self.j]) % 256])
        return bytes(out)

    def decrypt(self, data):
        return self.encrypt(data)

class AES:
    def __init__(self, key, mode):
        raise NotImplementedError()
