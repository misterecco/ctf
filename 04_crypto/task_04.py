from pwn import *
import math


FLAG_NUMBERS = [0, 1, 123, 0x7F4B81BE, 0xDB3BE6B0, 0xFFFFFFFF]


class Decryptor():
    def __init__(self):
        self.p = process("./src/crypto_homework_2")
        # self.p = remote('p4.team', 8403)
        self.p.recvuntil("Ready!")

        self.p.send("0<1\n")
        self.p.recvline()
        first_cand_0 = int(self.p.recvline())

        self.p.send("1<0\n")
        snd_cand_0 = int(self.p.recvline())

        self.p.send("{}+{}\n".format(first_cand_0, snd_cand_0))
        enc_one = int(self.p.recvline())

        enc_zero = snd_cand_0 if first_cand_0 == enc_one else first_cand_0

        self.p.send('{}+{}\n'.format(enc_zero, enc_zero))
        zero = int(self.p.recvline())

        assert(enc_zero == zero)

        self.encodings = {
            0: enc_zero,
            1: enc_one,
        }
        print(self.encodings)


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
            fst = 2 ** int(math.log(num, 2))            
            enq = [(fst, num-fst)]
            while len(enq) > 0:
                (f, s) = enq[-1]
                if s in self.encodings and (f+s) not in self.encodings:
                    ef = self.encrypt_number(f)
                    es = self.encrypt_number(s)
                    self.p.send("{}+{}\n".format(ef, es))
                    en = int(self.p.recvline())
                    self.encodings[f+s] = en
                    enq.pop()
                elif s not in self.encodings:
                    fst = 2 ** int(math.log(s, 2))
                    enq.append((fst, s-fst))
            return self.encodings[num]


    def decrypt_number(self, num):
        zero = self.encodings[0]
        one = self.encodings[1]
        def bin_search(start, end):
            if start == end:
                return start
            middle = (start + end) / 2
            m = self.encrypt_number(middle)
            self.p.send("{}<{}\n".format(m, num))
            r = int(self.p.recvline())
            if r == one:
                return bin_search(middle + 1, end)
            else:
                return bin_search(start, middle)
        
        return bin_search(0, 0xFFFFFFFF)
        
        
    def prepare_numbers_for_first_flag(self):
        self.answers = {}
        for num in FLAG_NUMBERS:
            n = self.decrypt_number(num)
            self.answers[num] = n


    def get_easy_flag(self):
        self.p.send("0>0\n")

        line = self.p.recvline()
        print(line)
        line = self.p.recvline()
        print(line)

        for i in FLAG_NUMBERS:
            self.p.recvuntil(" == ")
            print("{} <- {}".format(i, self.answers[i]))
            ans = "{}\n".format(self.answers[i])
            self.p.send(ans)
        
        res = self.p.recvuntil("keys:")
        print(res)


def solve():
    d = Decryptor()
    d.prepare_encodings()
    d.prepare_numbers_for_first_flag()
    d.get_easy_flag()


if __name__ == '__main__':
    solve()