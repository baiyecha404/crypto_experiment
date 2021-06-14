# coding: utf-8
# -**- author: byc_404 -**-
import string
from collections import Counter

char_list = string.ascii_lowercase


def ext_gcd(a, b):
    if b == 0:
        return 1, 0, a
    x, y, r = ext_gcd(b, a % b)
    temp = x
    x = y
    y = temp - int(a / b) * y
    return x, y, r


def getparam(a, b):
    m = ext_gcd(a, 26)[0] % 26
    return m, -b * m % 26


def affine(msg, a, b):
    res = ''.join([char_list[(a * char_list.index(x) + b) % 26] for x in msg])
    return res


if __name__ == '__main__':
    plaintext = 'In several distributed systems a user should only be able to access data if a user posses a certain set of credentials or attributes Currently the only method for enforcing such policies is to employ a trusted server to store the data and mediate access control However if any server storing the data is compromised then the confidentiality of the data will be compromised In this paper we present a system for realizing complex access control on encrypted data that we call ciphertext-policy attribute-based encryption By using our techniques encrypted data can be kept confidential even if the storage server is untrusted moreover our methods are secure against collusion attacks'.lower().replace(' ','').replace('-','')
    a, b = 11, 6
    cipher = affine(plaintext, a, b)
    print(cipher)
    print(Counter(cipher))
    m, n = getparam(a, b)
    plain = affine(cipher, m, n)
    print(plain)
    print(Counter(plain))

