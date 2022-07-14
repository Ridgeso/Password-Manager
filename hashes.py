from random import choices, choice

class Hash:
    def create_password(self):
        alphC = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alphL = "abcdefghijklmnopqrstuvwxyz"
        sings = "!#$%&`()*+,-./:;<=>?@[\\]^_{|}"
        nums  = "0123456789"
        pa    = ""

        for _ in range(5):
            paset = choices((alphC, alphL, sings, nums), weights=(1, 2, 3, 1), k=4)
            for ran in paset:
                pa += choice(ran)
        return pa


    def decrypt(self, pa):
        new = ""
        for s in pa:
            n = ord(s)
            n ^= (pow(2, n.bit_length()-1)-1)
            new += hex(n)[2:]
        return new


    def encrypt(self, pa):
        old = ""
        pa = iter(pa)
        for s, k in zip(pa, pa):
            n = int(s+k, 16)
            n ^= (pow(2, n.bit_length()-1)-1)
            old += chr(n)
        return old
