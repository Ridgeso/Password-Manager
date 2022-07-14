from random import choices, choice


class AEV:
    """TODO: implement AEV hashing algorithm"""
    pass


class Hash:
    __slots__ = "aev",

    def __init__(self) -> None:
        self.aev = AEV()

    def create_password(self):
        alphC    = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        alphL    = "abcdefghijklmnopqrstuvwxyz"
        sings    = "!#$%&`()*+,-./:;<=>?@[\\]^_{|}"
        nums     = "0123456789"
        password = ""

        for _ in range(5):
            password_fragment = choices((alphC, alphL, sings, nums), weights=(1, 2, 3, 1), k=4)
            for random_character in password_fragment:
                password += choice(random_character)
        return password

    def decrypt(self, password):
        new_password = ""
        for character in password:
            baits = ord(character)
            baits ^= (pow(2, baits.bit_length()-1)-1)
            new_password += hex(baits)[2:]
        return new_password

    def encrypt(self, password):
        old_password = ""
        password = iter(password)
        for char1, char2 in zip(password, password):
            baits = int(char1+char2, 16)
            baits ^= (pow(2, baits.bit_length()-1)-1)
            old_password += chr(baits)
        return old_password
