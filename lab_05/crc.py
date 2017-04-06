from zlib import crc32
import socket

'''f = lambda x: x if x >= 0 else 2**32 - x
for i in range(256):
    if f(crc32(chr(i))) < 256:
        print(i)
import sys
sys.exit()'''

def to_LE(x, k):
    result = 0
    for i in range(k):
        d = x // (2 ** (8 * i))
        d %= 256
        result += d * (2 ** (8 * (k - i - 1)))
    return result

conn = socket.create_connection(('p4.team', 8401))

f = conn.makefile()

a = int(f.readline(), base=16)

def send_number(n):
    # print("%x" % n)
    print("%.20x" % n) # wiadomosc o dlugosci 10 bajtow
    f.write("%x\n" % n)
    f.flush()
    r = f.readline()
    print(r)
    return r


def send_msg(m):
    d = crc32("%x" % m) ^ (a // (2 ** 32))
    d = to_LE(d, 4)
    an1 = a ^ (m * (2 ** 32))
    an2 = an1 ^ d
    send_number(an2)

# send_msg(100)

# send_number(a)

for n in range(256):
    x = send_number(256 * (a ^ sum(2**(32+i) for i in range(8))) + n)
    if x.startswith('OK'):
        break

d = crc32(b'\x00')^crc32(b'\x01') # 0x77073096

d = to_LE(d, 4)


an1 = a ^ 2 ** 32
an2 = an1 ^ d

send_number(an2)
