# coding: utf-8
# -**- author: byc_404 -**-
from utils import *


class SelfRSA:

    def __init__(self):
        self.e = self.d = self.n = self.p = self.q = self.phi = 0

    def __egcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = self.__egcd(b % a, a)
            return g, x - (b // a) * y, y

    def __modinv(self, a, m):
        g, x, y = self.__egcd(a, m)
        if g != 1:
            raise Exception("modular inverse doesn't exist")
        else:
            return x % m

    def __pow(self, a, b, mod):
        res = 1
        while b:
            if b & 1:
                res = (res * a) % mod
            a = (a * a) % mod
            b >>= 1
        return res

    def encrypt(self, msg, keypair) -> int:
        if keypair is None:
            keypair = (self.e, self.n)
        msg = int.from_bytes(msg.encode(), 'big')
        return self.__pow(msg, keypair[0], keypair[1])

    def decrypt(self, cipher, keypair) -> int:
        if keypair is None:
            keypair = (self.d, self.n)
        return self.__pow(cipher, keypair[0], keypair[1])

    def generateKey(self, bits, e=65537):
        self.p = genPrime(bits)
        self.q = genPrime(bits)

        self.n = self.p * self.q
        self.phi = (self.p - 1) * (self.q - 1)
        self.e = e
        self.d = self.__modinv(self.e, self.phi)

    def getPrivateKey(self):
        return self.d, self.n

    def getPublicKey(self):
        return self.e, self.n


if __name__ == "__main__":
    r = SelfRSA()
    r.generateKey(1024)
    pubkey, privkey = r.getPublicKey(), r.getPrivateKey()

    msg = "byc_404_2333"
    cipher = r.encrypt(msg, pubkey)
    plaintext = r.decrypt(cipher, privkey)

    assert int.from_bytes(msg.encode(), 'big') == plaintext
    print(f'Encrypted: {cipher}')
    print(f'Decrypted: {plaintext}')