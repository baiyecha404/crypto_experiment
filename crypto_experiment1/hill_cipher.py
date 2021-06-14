# coding: utf-8
# -**- author: byc_404 -**-
import string
import numpy as np
from sympy import Matrix
from collections import Counter

char_list = string.ascii_lowercase

key = np.mat([[10, 5, 12, 0, 0], [3, 14, 21, 0, 0], [8, 9, 11, 0, 0], [0, 0, 0, 11, 8], [0, 0, 0, 3, 7]])
key_matrix = Matrix(key)
reverse_key_matrix = np.mat(key_matrix.inv_mod(26).tolist())

LEN = len(key.tolist()[0])


def text2matrix(text):
    text_array = []
    messages = [text[i: i + LEN] for i in range(0, len(text), LEN)]
    for message in messages:
        tmp = []
        for i in range(LEN):
            tmp.append(char_list.index(message[i]))
        text_array.append(tmp)
    return np.mat(text_array).T


def matrix2text(ans):
    res = ''
    for group in ans.tolist():
        res += ''.join([char_list[i] for i in group])
    return res


def hill(text, key):
    return key * text % 26

def analysis(text):
    return  Counter(text)


if __name__ == '__main__':
    plaintext = 'In several distributed systems a user should only be able to access data if a user posses a certain set of credentials or attributes Currently the only method for enforcing such policies is to employ a trusted server to store the data and mediate access control However if any server storing the data is compromised then the confidentiality of the data will be compromised In this paper we present a system for realizing complex access control on encrypted data that we call ciphertext-policy attribute-based encryption By using our techniques encrypted data can be kept confidential even if the storage server is untrusted moreover our methods are secure against collusion attacks'.lower().replace(
        ' ', '').replace('-', '')
    plaintext_matrix = text2matrix(plaintext)
    ans = hill(plaintext_matrix, key_matrix)
    cipher = matrix2text(ans.T)
    print(cipher)
    print(analysis(cipher))

    cipher_matrix = text2matrix(cipher)
    plain = hill(cipher_matrix, reverse_key_matrix)
    plain = matrix2text(plain.T)
    print(plain)
    print(analysis(plain))