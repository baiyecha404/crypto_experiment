# coding: utf-8
# -**- author: byc_404 -**-
import struct
from hashlib import sha1


class SelfSha1:
    hash_set = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476, 0xc3d2e1f0]
    mask = 0xffffffff

    def __init__(self, msg: str):
        self.msg = msg.encode()

    def _padding(self):
        """
        process the message to 512 bit
        :return:
        """
        msgLen = len(self.msg)
        pad = msgLen % 64
        paddingLen = (56 - pad) % 64

        self.msg += b"\x80"
        self.msg += b"\x00" * (paddingLen - 1)
        msgLen = msgLen * 8
        self.msg += struct.pack(">Q", msgLen)

    def _leftRot(self, value: int, n: int) -> int:
        """
        left rotate the value with n bit
        :param value: input bytes
        :param n: shift bytes
        :return: shifted result
        """
        return value << n & self.mask | value >> (32 - n)  # 32bit shift left

    def _proccess(self, chunks: list[bytes]):
        """
        process each chunk, update the hashset (the set of registers)
        :return: None
        """
        # ref:https://en.wikipedia.org/wiki/SHA-1
        f, k = 0, 0
        for chunk in chunks:
            # break chunk into sixteen 32-bit big-endian words w[i]
            w = list(struct.unpack(">16L", chunk))
            for i in range(16, 80):
                # Message schedule: extend the sixteen 32-bit words into eighty 32-bit words:
                val = w[i - 3] ^ w[i - 8] ^ w[i - 14] ^ w[i - 16]
                w.append(self._leftRot(val, 1))

            a, b, c, d, e = self.hash_set
            for i in range(len(w)):
                if i < 20:
                    f = (b & c) | (self._not(b) & d)
                    k = 0x5a827999
                elif i < 40:
                    f = b ^ c ^ d
                    k = 0x6ed9eba1
                elif i < 60:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8f1bbcdc
                elif i < 80:
                    f = b ^ c ^ d
                    k = 0xca62c1d6

                tmp = (self._leftRot(a, 5) + f + e + k + w[i]) & self.mask
                e, d, c, b, a = d, c, self._leftRot(b, 30), a, tmp

            r_set = [a, b, c, d, e]
            self.hash_set = [((m + n) & self.mask) for m, n in zip(self.hash_set, r_set)]

    def hexdigest(self) -> str:
        """
        process and calculate the digest, then return the hash in hex
        :return: the hexdigest of result
        """
        self._padding()
        chunks = [self.msg[i: 64 + i] for i in range(0, len(self.msg), 64)]
        self._proccess(chunks)
        return "".join(f"{h:08x}" for h in self.hash_set)

    @staticmethod
    def _not(num: int) -> int:
        """
        :param num: input number
        :return:  the reverse of num
        """
        r = 0
        for _ in range(32):
            r = r << 1
            high = (num & 0x80000000) >> 31
            r ^= 1
            r ^= high
            num = num << 1
            num &= 0xffffffff
        return r


if __name__ == '__main__':
    data = 'Beijing University of Posts and Telecommunications'
    assert SelfSha1(data).hexdigest() == sha1(data.encode()).hexdigest()
    print(f'input: {data}')
    print(f'hash of input: {SelfSha1(data).hexdigest()}')