"""
hash.py is module for simple creating random password and
for decrypting it and encrypting
"""
from random import choices, choice


def create_password():
    """Create a random password of length 20 characters"""
    alphC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    alphL = "abcdefghijklmnopqrstuvwxyz"
    sings = "!#$%&`()*+,-./:;<=>?@[\\]^_{|}"
    nums  = "0123456789"
    pa    = ""

    for _ in range(5):
        """
        This list is randomly choosing sets of charactes
        and for every set of them algorithm chooses one
        and makes with it password
        """
        paset = choices((alphC, alphL, sings, nums), weights=(1, 2, 3, 1), k=4)
        for ran in paset:
            pa += choice(ran)
    return pa


def decrypt(pa):
    """
    This function takes a pa and throws each character
    throgh bitwise XOR operator of 15 and returns a
    string of a hexadecimal values of length 2 each
    pa: string
    """
    new = ""
    for s in pa:
        n = ord(s)
        n ^= (pow(2, n.bit_length()-1)-1)
        new += hex(n)[2:]
    return new


def encrypt(pa):
    """
    This function takes a pa and throws each 2 characters
    as a integer throgh bitwise XOR operator of 15 and
    returns a string
    pa: string
    """
    old = ""
    pa = iter(pa)
    for s, k in zip(pa, pa):
        n = int(s+k, 16)
        n ^= (pow(2, n.bit_length()-1)-1)
        old += chr(n)
    return old


# def getbin(n, k):
#     print(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF)
#     return format(n, "b").zfill(k)
