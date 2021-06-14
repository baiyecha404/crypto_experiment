# coding: utf-8
# -**- author: byc_404 -**-

def replacement(msg, cur_key):
    ans = ''
    for i in range(0, len(msg), 7):
        text = msg[i: i + 7]
        ans += ''.join(text[cur_key[i] - 1] for i in range(len(text)))
    return ans


def encrypt(message, key):
    if len(message) % 7 != 0:
        message += '0' * (7 - len(message) % 7)  # padding with '0'
    return replacement(message, key)


def decrypt(cipher, key):
    dec = []
    for i in range(1, 1 + 7):
        dec.append(key.index(i) + 1)
    return replacement(cipher, dec).rstrip('0')


if __name__ == '__main__':
    plaintext = """In several distributed systems a user should only be able to access data if a user posses a certain set of credentials or attributes Currently the only method for enforcing such policies is to employ a trusted server to store the data and mediate access control However if any server storing the data is compromised then the confidentiality of the data will be compromised In this paper we present a system for realizing complex access control on encrypted data that we call ciphertext-policy attribute-based encryption By using our techniques encrypted data can be kept confidential even if the storage server is untrusted moreover our methods are secure against collusion attacks""".replace(' ', '')
    key = [5, 3, 7, 4, 1, 2, 6]
    print(encrypt(plaintext, key))
    print(decrypt(encrypt(plaintext, key), key))
