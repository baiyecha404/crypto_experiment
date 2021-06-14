# coding: utf-8
# -**- author: byc_404 -**-
import random


def rabinMillerPassed(mrc, rabin_miller_rounds):
    """
    Run iterations of Rabin Miller Primality test
    https://www.geeksforgeeks.org/how-to-generate-large-prime-numbers-for-rsa-algorithm/
    """
    maxDivisionsByTwo = 0
    ec = mrc - 1
    while ec % 2 == 0:
        ec >>= 1
        maxDivisionsByTwo += 1
    assert (2 ** maxDivisionsByTwo * ec == mrc - 1)

    def trialComposite(round_tester):
        if pow(round_tester, ec, mrc) == 1:
            return False
        for i in range(maxDivisionsByTwo):
            if pow(round_tester, 2 ** i * ec, mrc) == mrc - 1:
                return False
        return True

    # Set number of trials here
    for i in range(rabin_miller_rounds):
        round_tester = random.randrange(2, mrc)
        if trialComposite(round_tester):
            return False
    return True


def genPrime(bits):
    while True:
        p = random.getrandbits(bits)
        while p & 1 == 0:
            p = random.getrandbits(bits)
        # prime test
        rabin_miller_rounds = 10
        if rabinMillerPassed(p, rabin_miller_rounds):
            return p
