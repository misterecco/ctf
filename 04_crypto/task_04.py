from pwn import *
import math
import sys


sys.setrecursionlimit(10000)


class Decryptor():
    def __init__(self):
        self.p = process("./src/crypto_homework_2")
        self.p.recvuntil("Ready!")

        self.p.send("0<1\n")
        self.p.recvline()
        first_cand_0 = int(self.p.recvline())

        self.p.send("1<0\n")
        snd_cand_0 = int(self.p.recvline())

        self.p.send("{}+{}\n".format(first_cand_0, snd_cand_0))
        enc_one = int(self.p.recvline())

        enc_zero = snd_cand_0 if first_cand_0 == enc_one else first_cand_0

        self.encodings = {
            0: enc_zero,
            1: enc_one,
        }

    def prepare_encodings(self):
        for n in [2 ** i for i in range(1,33)]:
            n2 = n / 2
            n2e = self.encodings[n2]
            self.p.send("{}+{}\n".format(n2e, n2e))
            self.encodings[n] = int(self.p.recvline())

    def encrypt_number(self, num):
        if num in self.encodings:
            return self.encodings[num]
        else:
            first = int(math.log(num, 2))
            snd = num - first
            ef = self.encrypt_number(first)
            es = self.encrypt_number(snd)
            en = self.p.send("{}+{}\n".format(ef, es))
            en = int(self.p.recvline())
            self.encodings[num] = en
            return en

    def prepare_numbers_for_first_flag(self):
        for num in [0, 1, 123, 0x7F4B81BE, 0xDB3BE6B0, 0xFFFFFFFF]:
            self.encrypt_number(num)

    def finish(self):
        self.p.send("0>0\n")

        count = self.p.recvline()
        print(count)
        self.p.recvline()


def solve():
    d = Decryptor()

    print(d.encodings)
    d.prepare_encodings()
    print(d.encodings)

    d.prepare_numbers_for_first_flag()
    print(d.encodings)

    d.finish()


if __name__ == '__main__':
    solve()